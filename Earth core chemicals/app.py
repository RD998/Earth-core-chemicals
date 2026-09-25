from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

name = ""
address = ""
number = ""
item_name = ""
total_price = 0

data2 = {
    "item_name": [],
    "quantity": [],
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/customer")
def customer_dashboard():
    count = countig(name)
    return render_template("customer_dashboard.html", count=count)

@app.route("/customer_detai")
def customer_details():
    return render_template("customer_details.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "RD" and password == "1300135":
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid username or password")
    return render_template("admin_login.html")

@app.route("/details", methods=["GET", "POST"])
def detailsig():
    global name, address, number
    if request.method == "POST":
        name = request.form["Name"]
        address = request.form["address"] + "      "
        number = request.form["number"]
        return redirect(url_for("customer_dashboard"))
    else:
        return redirect(url_for("customer_details"))

@app.route('/place_order', methods=['POST'])
def place_order():
    global item_name, total_price, name, address, number
    item_name = request.form.get("item_name") 
    quantity = int(request.form.get("quantity"))  
    count = countig(name) + 1
    data = []
    
    with open("products.csv", "r") as f:
        lines1 = f.readlines()

    header = lines1[0].strip().split(",")
    for line in lines1[1:]:
        parts = line.strip().split(",")
        data.append(parts)

    found = False
    total_price = 0
    for row in data:
        # Safety check to prevent index crashes on empty lines
        if len(row) < 3: 
            continue
            
        Item = row[0]
        Quantity = int(row[1])
        Price = int(row[2])

        if Item.lower() == item_name.lower():
            found = True
            if quantity <= Quantity:
                total_price = quantity * Price
                print("Product available")
                print("Total price:", total_price)
            else:
                print("Only", Quantity, "units available")
            break

    if not found:
        print("Product not found")
        return render_template("customer_dashboard.html", count=count, error="Product not found")
    
    if count == 10:
        total_price = 0
    
    with open("purchases.csv", "a+") as f:
        SNo = 0
        f.seek(0)
        data56 = csv.reader(f)
        for row in data56:
            if row: 
                SNo += 1
        if SNo > 0:
            SNo = SNo - 1
        f.write(f"{SNo},{name},{number},{address},{item_name},{total_price}\n")

    return render_template("customer_dashboard.html", count=count)

@app.route("/admin_dashboard")
def admin_dashboard():
    with open("purchases.csv", "r") as f:
        lines = f.readlines()
    
    if lines and not lines[0].strip()[0].isdigit():
        lines = lines[1:]

    global data2
    data2 = {
        "SNo": [], "name": [], "number": [], "address": [], "item_name": [], "total_price": []
    }

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) >= 6:  
            data2["SNo"].append(parts[0])
            data2["name"].append(parts[1])
            data2["number"].append(parts[2])
            data2["address"].append(parts[3])
            data2["item_name"].append(parts[4])
            data2["total_price"].append(int(parts[5]))

    headers = list(data2.keys())

    html = "<center><table></center>\n"
    html += "  <tr>\n"
    for header in headers:
        html += f"    <th>{header}</th>\n"
    html += "  </tr>\n"

    rows_count = len(data2[headers[0]]) if headers else 0
    for i in range(rows_count):
        html += "  <tr>\n"
        for header in headers:
            html += f"    <td>{data2[header][i]}</td>\n"
        html += "  </tr>\n"

    html += "</table>"

    return render_template("admin_dashboard.html", data2=data2, html=html)

def countig(check_name):
    if not check_name: 
        return 0
    with open("purchases.csv", "r") as file:
        file.seek(0)
        v = csv.reader(file)
        za = 0
        for row in v:
            if len(row) > 1 and row[1].strip().lower() == check_name.strip().lower():
                za += 1
        return za

if __name__ == '__main__':
    app.run(debug=True)
