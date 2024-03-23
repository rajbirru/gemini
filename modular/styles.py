# Define a function to return the stylesheet for the app
def load_styles():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #F0F3F4;
    }
    .container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2 {
        color: #2E86C1;
    }
    input, select, .stSlider {
        border: 1px solid #D0D3D4;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        width: 100%;
        box-sizing: border-box;
    }
    button {
        background-color: #2E86C1;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    button:hover {
        background-color: #14659E; /* Slightly darker on hover */
    }
    </style>
    """
