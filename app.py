from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from analyzer import DataAnalyzer
from visualizer import DataVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/images", exist_ok=True)

logger.info("✓ App initialized successfully")


def allowed_file(filename):
    """Check if file is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Home page"""
    logger.info("GET / - Home page accessed")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload"""
    logger.info("POST /upload - File upload initiated")

    try:
        if "file" not in request.files:
            logger.warning("⚠ No file provided in request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            logger.warning("⚠ No file selected")
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            logger.warning(f"⚠ Invalid file type: {file.filename}")
            return jsonify({"error": "Only CSV files allowed"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        logger.info(f"✓ File uploaded: {filename}")

        # Analyze data
        analyzer = DataAnalyzer(filepath)
        if analyzer.df is None:
            logger.error("✗ Failed to load data")
            return jsonify({"error": "Failed to load data"}), 400

        overview = analyzer.get_overview()

        logger.info(
            f"✓ Analysis completed: {overview['rows']} rows, {overview['columns']} columns"
        )

        return jsonify(
            {"status": "success", "filename": filename, "overview": overview}
        )

    except Exception as e:
        logger.error(f"✗ Upload error: {str(e)}")
        return jsonify({"error": str(e)}), 400


@app.route("/analysis/<filename>")
def analysis(filename):
    """Get data analysis"""
    logger.info(f"GET /analysis/{filename}")

    try:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))

        if not os.path.exists(filepath):
            logger.warning(f"⚠ File not found: {filename}")
            return jsonify({"error": "File not found"}), 404

        analyzer = DataAnalyzer(filepath)

        analysis_data = {
            "overview": analyzer.get_overview(),
            "statistics": analyzer.get_statistics(),
            "head": analyzer.get_head(10),
            "tail": analyzer.get_tail(10),
            "numeric_columns": analyzer.get_numeric_columns(),
            "categorical_columns": analyzer.get_categorical_columns(),
        }

        logger.info("✓ Analysis data retrieved")
        return render_template("analysis.html", data=analysis_data, filename=filename)

    except Exception as e:
        logger.error(f"✗ Analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/visualize", methods=["POST"])
def api_visualize():
    """API endpoint for visualizations"""
    logger.info("POST /api/visualize")

    try:
        data = request.json
        filename = data.get("filename")
        chart_type = data.get("chart_type")
        column = data.get("column")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))

        if not os.path.exists(filepath):
            logger.warning(f"⚠ File not found: {filename}")
            return jsonify({"error": "File not found"}), 404

        analyzer = DataAnalyzer(filepath)
        visualizer = DataVisualizer(analyzer.df)

        chart_file = None

        if chart_type == "histogram" and column:
            chart_file = visualizer.histogram(column, f"hist_{filename}_{column}.png")

        elif chart_type == "scatter" and analyzer.get_numeric_columns():
            cols = analyzer.get_numeric_columns()
            chart_file = visualizer.scatter_plot(
                cols[0],
                cols[1] if len(cols) > 1 else cols[0],
                f"scatter_{filename}.png",
            )

        elif chart_type == "correlation":
            chart_file = visualizer.correlation_heatmap(f"heatmap_{filename}.png")

        elif chart_type == "boxplot" and column:
            chart_file = visualizer.box_plot(column, f"box_{filename}_{column}.png")

        elif chart_type == "line" and column:
            chart_file = visualizer.line_chart(column, f"line_{filename}_{column}.png")

        elif chart_type == "bar" and column:
            chart_file = visualizer.bar_chart(column, f"bar_{filename}_{column}.png")

        elif chart_type == "distribution" and column:
            chart_file = visualizer.distribution_plot(
                column, f"dist_{filename}_{column}.png"
            )

        else:
            logger.warning(f"⚠ Invalid chart type or missing column: {chart_type}")
            return jsonify({"error": "Invalid chart type"}), 400

        if not chart_file:
            logger.error("✗ Chart generation failed")
            return jsonify({"error": "Chart generation failed"}), 400

        logger.info(f"✓ Chart created: {chart_file}")
        return jsonify({"status": "success", "chart": chart_file})

    except Exception as e:
        logger.error(f"✗ Visualization error: {str(e)}")
        return jsonify({"error": str(e)}), 400


@app.route("/health")
def health():
    """Health check endpoint"""
    logger.info("GET /health")
    return jsonify({"status": "healthy", "message": "App is running"})


@app.errorhandler(404)
def not_found(error):
    logger.warning(f"⚠ 404 error: {request.path}")
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"✗ 500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("🚀 Starting Data Analytics App")
    logger.info("=" * 50)
    app.run(debug=True, port=5000)
