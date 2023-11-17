from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import csv
from RPA.PDF import PDF
from RPA.Archive import Archive


@task
def robot_order_automation():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=50,
    )
    access_order_url()
    accept_warnings()
    show_model_info()
    download_csv()
    fill_form_from_csv()
    create_a_zip_output_folder()
    
@task
def robot_order_automation_II():
    """A test task to see if is possible run a variety of tasks in a same doc
    See if is possible to click at button 'No way' """

    page = browser.page()

    access_order_url()
    page.click("button:text('No way')")

def access_order_url():
    """Navigates to the URL site that order a Robot"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def accept_warnings():
    """Clicks in OK at acceptance warning after clicks in No way button"""
    page = browser.page()
    page.click("button:text('No way!')")
    page.click("button:text('OK')")

def show_model_info():
    """Show the model's informations area"""
    page = browser.page()
    page.click("button:text('Show model info')")

def fill_form(head_rep, body_rep, legs_rep, address_rep, rep):
    """Fill the form with the robots assembly preferences and generates the order report"""
    page = browser.page()
    page.select_option("//select[@id='head']", str(head_rep))
    page.click(f"//input[@id='id-body-{body_rep}']")
    page.fill("//input[@placeholder='Enter the part number for the legs']", str(legs_rep))
    page.fill("//input[@id='address']", str(address_rep))
    page.click("//button[@id='order']")
    error_handling()
    export_as_pdf(rep)
    page.screenshot(path=f"output/order_{rep}.png")

    page.click("button:text('Order another robot')")


def download_csv():
    """Downloads and save the csv with delivery data"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv",target_file="output", overwrite=True)

def fill_form_from_csv():
    """Take the csv's infos and does the orders from it using a FOR structure"""
    with open("output/orders.csv", "r") as orders:
        orders_csv = csv.reader(orders, delimiter=",")

        for i, row in enumerate(orders_csv):
           
            head = row[1]
            body = row[2]
            legs = row[3]
            address = row[4]
            rep = i

            if i!=0:
                fill_form(head, body, legs, address, rep)
                if i <= orders_csv.line_num:
                    accept_warnings()
                

            print("#Valor-Cabeca : " + str(head))
            if i==0:
                print("Cabecalho: " + "i: " + str(i) + str(row))
            else:
                print("Valor: " + "i: " + str(i) + str(row))

def export_as_pdf(k):
    """Export the data to a pdf file"""
    page = browser.page()
    receipt_results_html = page.locator("#receipt").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(receipt_results_html, f"output/order{k}_receipt_results.pdf")

def create_a_zip_output_folder():
    """Create a zip output folder of the output directory with all data inside"""
    data = Archive()
    data.archive_folder_with_zip(folder="output",archive_name="compressed_files.zip",compression="stored")

def error_handling():
    """Catch the error message and passes throught it trying to cliks many times as are nessessary at 'order' button"""
    page = browser.page()
    thereIsA_alert = page.is_visible("//*[@class='alert alert-danger']")
    print(thereIsA_alert)

    while thereIsA_alert:
        page.click("//button[@id='order']")
        thereIsA_alert = page.is_visible("//*[@class='alert alert-danger']")
        print(thereIsA_alert)



