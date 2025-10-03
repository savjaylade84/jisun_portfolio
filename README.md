# Jisun Portfolio

A personal portfolio website showcasing my projects, skills, and contact information.  

## 🌐 Live Website

[View the Portfolio](https://savjalade84.pythonanywhere.com/)

---

## Features

- **Responsive Design:** Works on desktop and mobile devices.
- **Project Showcase:** Highlights selected works and projects.
- **Contact Form:** Visitors can send messages directly via the “Let’s Connect” form.
- **Easy Customization:** Built with Flask and Python for simple updates and expansion.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templating)
- **Email:** SMTP (Gmail) for contact form
- **Hosting:** [PythonAnywhere](https://www.pythonanywhere.com/)

---

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/savjaylade84/jisun_portfolio.git
    cd jisun_portfolio
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**  
   Create a `.env` file in the project root with your email credentials:
    ```
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_gmail_app_password
    MAIL_RECEIVER=your_email@gmail.com
    MAIL_USE_TLS=false
    MAIL_USE_SSL=true
    MAIL_DEFAULT_SENDER=your_email@gmail.com
    MAIL_DEBUG=0
    TESTING=false
    MAIL_SUPPRESS_SEND=false
    ```

4. **Run the app locally:**
    ```bash
    python app.py
    ```

5. **Visit:**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment

This project is hosted on [PythonAnywhere](https://www.pythonanywhere.com/).  
For deployment instructions, see the [PythonAnywhere Flask deployment guide](https://help.pythonanywhere.com/pages/Flask/).

---

## License

This project is for personal and educational use.  
Feel free to fork and adapt for your own portfolio.

---

## Contact

For questions, suggestions, or collaboration, please use the contact form on the website.

---