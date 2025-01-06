# MedixTools Web Application

MedixTools is a lightweight and user-friendly web application designed for healthcare professionals, researchers, and students. It provides essential calculators and tools such as Z-score calculators, Light's Criteria, Ideal Body Weight (IBW) estimations, and more to assist in medical decision-making.

---

## Features

- **WHO Z-score Calculator**:
  - Calculate BMI-for-age, Weight-for-age, Length/Height-for-age, and Weight-for-Length/Height based on WHO growth standards.
  - Supports input for gender, age, height, weight, and measurement type (standing or recumbent).
  
- **Light's Criteria**:
  - Determine if pleural fluid is exudative or transudative.
  - Unit conversion between g/L and g/dL for convenience.

- **Ideal Body Weight (IBW)**:
  - Includes Devine formula for adults and Adjusted Body Weight (ABW) formula for obese children.

- **Dynamic User Interface**:
  - Sidebar for seamless navigation between calculators.
  - Fixed header and sidebar for consistent layout.
  - Smooth transitions between pages.

- **Custom Alerts**:
  - Custom modal with zoom-in and zoom-out animations for user notifications.

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask framework)
- **Deployment**: Docker, Render, GitHub

---

## Installation and Setup

### 1. Clone the Repository
```bash
$ git clone https://github.com/yourusername/MedixTools.git
$ cd MedixTools
```

### 2. Set Up Virtual Environment
```bash
$ python -m venv venv
$ source venv/bin/activate   # For Linux/Mac
$ venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
```bash
$ pip install -r requirements.txt
```

### 4. Run the Application
```bash
$ flask run
```
Visit the app at: `http://127.0.0.1:5000`

### 5. Docker Deployment (Optional)
Build and run the app using Docker:
```bash
$ docker build -t medix-tools .
$ docker run -p 5000:5000 medix-tools
```

---

## Usage

1. Open the application in your browser.
2. Use the sidebar to navigate between calculators.
3. Enter the required inputs and get instant results.

---

## File Structure

```
MedixTools/
|-- app.py              # Flask application
|-- templates/
|   |-- index.html      # Main landing page
|   |-- zscore-calculator.html  # Z-score calculator page
|-- static/
|   |-- styles.css      # Custom styles
|   |-- scripts.js      # JavaScript logic
|-- growthstandards/    # WHO growth standard data files
|-- requirements.txt    # Python dependencies
|-- Dockerfile          # Docker configuration
|-- README.md           # Project documentation
```

---

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

### Steps to Contribute
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- WHO Growth Standards Data
- Flask Framework Documentation
- OpenAI for Assistance in Development
