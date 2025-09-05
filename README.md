# Holy Cow Image Generator 🐄

A fun Flask web application that transforms your photos into the iconic "Holy Cow" style using Google's Gemini AI image generation model.

## Overview

This project uses Google's Gemini 2.5 Flash Image Preview model to generate stylized images by combining a user's uploaded photo with a reference "Holy Cow" image. The AI replaces the cow's head with the user's face while maintaining the distinctive artistic style and pose.

## Features

- **Web Interface**: Clean, responsive Flask web application
- **Image Upload**: Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP)
- **AI Image Generation**: Uses Google Gemini AI for style transfer and face replacement
- **Download Support**: Generated images can be downloaded directly
- **Error Handling**: Comprehensive logging and custom exception handling
- **Responsive Design**: Mobile-friendly interface

## Project Structure

```
Holy_Cow/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── setup.py                       # Package setup configuration
├── .env                           # Environment variables (API keys)
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
│
├── src/                           # Source code modules
│   ├── __init__.py
│   └── generator.py               # AI image generation logic
│
├── config/                        # Configuration files
│   ├── paths.py                   # File path configurations
│   └── __pycache__/
│
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── logger.py                  # Logging configuration
│   └── custom_exception.py        # Custom exception handling
│
├── Templates/                     # HTML templates
│   ├── index.html                 # Main page template
│   ├── uploaded.html              # Upload success page
│   └── result.html                # Result display page
│
├── artifacts/                     # Image storage
│   ├── original_holy_cow.png      # Reference cow image
│   ├── uploaded_image.png         # User uploaded image
│   └── generated_image.png        # AI generated result
│
├── logs/                          # Application logs
│   ├── log_2025-09-01.log
│   └── log_2025-09-05.log
│
├── holy_cow_env/                  # Virtual environment
└── Holy_Cow_Image_Gen.egg-info/   # Package metadata
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Holy_Cow
```

### 2. Create Virtual Environment

```bash
python -m venv holy_cow_env
source holy_cow_env/bin/activate  # On Windows: holy_cow_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_primary_gemini_api_key_here
FALLBACK_GEMINI_API_KEY=your_backup_gemini_api_key_here
```

### 5. Setup Project Structure

Ensure the `artifacts` directory contains the reference cow image:
- Place your reference cow image as `artifacts/original_holy_cow.png`

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the Web Interface

1. **Upload Image**: Navigate to the homepage and upload your photo
2. **Generate**: Click "Generate Holy Cow Image" to create the stylized version
3. **Download**: Save the generated image to your device

### API Endpoints

- `GET /` - Main page
- `POST /upload` - Upload user image
- `POST /generate` - Generate AI image
- `GET /artifacts/<filename>` - Serve static files

## Key Components

### Core Modules

- **[`app.py`](app.py)**: Main Flask application with routing and file handling
- **[`src/generator.py`](src/generator.py)**: AI image generation using Gemini API
- **[`config/paths.py`](config/paths.py)**: Centralized file path management
- **[`utils/logger.py`](utils/logger.py)**: Logging system with date-stamped files
- **[`utils/custom_exception.py`](utils/custom_exception.py)**: Enhanced error handling

### Image Processing Flow

1. User uploads image via web interface
2. Image saved to [`artifacts/uploaded_image.png`](artifacts/uploaded_image.png)
3. [`generate_image()`](src/generator.py) function processes both reference and user images
4. Gemini AI generates stylized image combining both inputs
5. Result saved as [`artifacts/generated_image.png`](artifacts/generated_image.png)

## Dependencies

Key packages from [`requirements.txt`](requirements.txt):

- **Flask 3.1.2**: Web framework
- **google-genai 1.32.0**: Google Gemini API client
- **Pillow 11.3.0**: Image processing
- **python-dotenv 1.1.1**: Environment variable management
- **werkzeug 3.1.3**: WSGI utilities

## Configuration

### File Paths

Configured in [`config/paths.py`](config/paths.py):
- `artifacts_path`: Image storage directory
- `cow_image_path`: Reference cow image location
- `uploaded_image_path`: User upload destination

### Logging

Configured in [`utils/logger.py`](utils/logger.py):
- Daily log files in `logs/` directory
- INFO level logging with timestamps
- Centralized logger creation via [`get_logger()`](utils/logger.py)

## Error Handling

The application uses a custom exception system ([`utils/custom_exception.py`](utils/custom_exception.py)) that provides:
- Detailed error messages with file names and line numbers
- Enhanced debugging information
- Consistent error logging throughout the application

## Development

### Adding New Features

1. Create new modules in appropriate directories (`src/`, `utils/`, etc.)
2. Follow the existing logging pattern using [`get_logger(__name__)`](utils/logger.py)
3. Use [`CustomException`](utils/custom_exception.py) for error handling
4. Update templates in `Templates/` directory for UI changes

### Testing

Run the application locally:
```bash
python app.py
```

Visit `http://localhost:5000` to test functionality.

## License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.

## Author

**Kabyik** - Initial work and development

## Acknowledgments

- Google Gemini AI for image generation capabilities
- Flask community for the web framework
- PIL/Pillow for image processing utilities

---

**Note**: This is a fun side project for entertainment purposes. Ensure you have proper API keys configured before running the application.