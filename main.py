from flask import Flask, render_template, request, jsonify, session
import logging

# Initialize Flask App------------------------------------------
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # For session management
#---------------------------------------------------------------

# Initialize Logger
logging.basicConfig(level=logging.INFO)

# Function to write to a file
def write_to_file(file_path, content):
    try:
        with open(file_path, "a") as f:
            f.write(content + "\n")
    except Exception as e:
        logging.exception("Error writing to file")

# Function to get bot response
def get_response():
    text = request.get_json().get('message').lower()

# New session, send a welcome message --------MAIN MENU-----------
    if session.get('state') is None:
        session['state'] = 'welcome'
        return "Please select an option below:\n1. Sell\n2. Buy\n3. Talk to a representative"

#talk to a representative---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if text == 'talk to a representative':
        session['state'] = 'waiting_for_email'
        return "Could you please provide your email so we can connect you to a representative?"

    if session['state'] == 'waiting_for_email':
        session['email'] = text
        session['state'] = 'waiting_for_phone'
        return "Could you please provide your phone number?"

    if session['state'] == 'waiting_for_phone':
        session['phone'] = text
        write_to_file("info.txt", f"User with email {session['email']} and phone {session['phone']} wants to talk to a representative.")
        session.clear()
        return "Thank you! A representative will contact you soon."

# Handling the 'sell' flow state transitions---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if text == 'sell':
        session['state'] = 'sell_property_type'
        return "What type of property do you want to sell? (Commercial, Residential, Project Development)"

    if session['state'] == 'sell_property_type':
        types = {'commercial': 'Commercial', 'residential': 'Residential', 'project development': 'Project Development'}
        session['property_type'] = types.get(text, 'Unknown')
        session['state'] = 'sell_location'
        return "Where is the property located?"

    if session['state'] == 'sell_location':
        session['location'] = text
        session['state'] = 'sell_price_range'
        return "What is the price range of this property?"

    if session['state'] == 'sell_price_range':
        session['price_range'] = text
        session['state'] = 'sell_rented'
        return "Is the property being rented? (yes/no)"

    if session['state'] == 'sell_rented':
        if text == 'yes':
            session['rented'] = 'Yes'
            session['state'] = 'sell_rent_amount'
            return "For how much is it being rented?"
        else:
            session['rented'] = 'No'
            session['state'] = 'sell_email'
            return "Please enter your email."

    if session['state'] == 'sell_rent_amount':
        session['rent_amount'] = text
        session['state'] = 'sell_email'
        return "Please enter your email."

    if session['state'] == 'sell_email':
        session['email'] = text
        session['state'] = 'sell_name'
        return "Can I know your name?"

    if session['state'] == 'sell_name':
        session['name'] = text
        if session['rented'] == 'Yes':
            write_to_file("info.txt", f"{session['name']} is interested in selling a {session['property_type']} property located in {session['location']}. The property falls within the price range of {session['price_range']}. Current rental status: {session['rented']}. Rent amount: {session['rent_amount']}\n\nContact information: {session['email']}")
        else:
            write_to_file("info.txt", f"{session['name']} is interested in selling a {session['property_type']} property located in {session['location']}. The property falls within the price range of {session['price_range']}. Which is not being rented. Email: {session['email']}")
        session.clear()
        return "Thank you for your details, we will get to you soon."
    
# Handling the 'sell' flow state transitions---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#border between sell and buy

# Handling the 'buy' flow state transitions---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if text == 'buy':
        session['state'] = 'buy_property_type'
        return "What type of property do you want to buy? (Commercial, Residential, Project Development)"

    if session['state'] == 'buy_property_type':
        session['property_type'] = text
        session['state'] = 'buy_location'
        return "In what location do you want to buy a property?"

    if session['state'] == 'buy_location':
        session['location'] = text
        session['state'] = 'buy_price_range'
        return "What is your price range?"

    if session['state'] == 'buy_price_range':
        session['price_range'] = text
        session['state'] = 'buy_email'
        return "Please enter your email"

    if session['state'] == 'buy_email':
        session['email'] = text
        session['state'] = 'buy_name'
        return "Can I know your name?"

    if session['state'] == 'buy_name':
        session['name'] = text
        write_to_file("info.txt", f"{session['name']} is looking to buy a {session['property_type']} property located in {session['location']}. The preferred price range for this property is {session['price_range']}. Contact information: {session['email']}")
        session.clear()
        return "Thank you for your details. We will get in touch with you soon."
# Handling the 'buy' flow state transitions---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/", methods=['GET'])
def index_get():
    logging.info("GET request for the index page.")
    return render_template('base.html')

@app.route("/predict", methods=['POST'])
def predict():
    try:
        response = get_response()
        return jsonify({"answer": response})
    except Exception as e:
        logging.exception("An error occurred while processing the request.")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
