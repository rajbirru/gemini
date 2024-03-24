# Define a function to return the stylesheet for the app
def load_styles():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');

    body {
        font-family: 'Raleway', sans-serif;
        background-color: #F0F3F4;
    }
    .container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2 {
        color: #2E86C1;
        transition: color 0.3s ease; /* Smooth transition for color changes */
    }
    h1:hover, h2:hover {
        color: #14659E; /* Darker shade on hover for headings */
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
        transition: background-color 0.3s ease; /* Smooth background transition for buttons */
    }
    button:hover {
        background-color: #14659E;
    }
    /* Special class for styling monetary values */
    .money {
        background-color: #f0f9ff; /* Very light blue background */
        color: #0366d6; /* Slightly darker blue for text */
        padding: 5px 10px; /* Smaller padding for a tag-like appearance */
        border-radius: 4px; /* Slightly rounded corners for a soft look */
        display: inline-block; /* Inline-block for use within text */
        margin: 0 5px; /* Small margin for spacing */
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }
    </style>
    """
