import json
import xlwt


with open('SF_businesses_details.json', "r") as j:
    list = json.load(j)

workbookw = xlwt.Workbook(encoding='utf-8')  # utf-8 
workbookw.default_style.font.height = 20 * 11
worksheetw = workbookw.add_sheet('SF')  # create new sheet

worksheetw.write(0, 0, "ID")
worksheetw.write(0, 1, "Name")
worksheetw.write(0, 2, "Display_address")
worksheetw.write(0, 3, "Zipcode")
worksheetw.write(0, 4, "Categories")
worksheetw.write(0, 5, "Review Count")
worksheetw.write(0, 6, "Rating")
worksheetw.write(0, 7, "Price")

n = 1
for k, v in list.items():
    # ID	Name	Display_address	Zipcode	Categories	Review Count	Rating	Price
    id = v["id"]
    name = v["name"]
    review = v["review_count"]
    rating = v["rating"]

    i = []
    for j in v["categories"]:
        i.append(j["title"])
    categories = ", ".join(i)

    address = " ".join(v["location"]["display_address"])
    zipcode = v["location"]["zip_code"]
    try:
        price = v["price"]
    except:
        price = ""
    worksheetw.write(n, 0, id)
    worksheetw.write(n, 1, name)
    worksheetw.write(n, 2, address)
    worksheetw.write(n, 3, str(zipcode))
    worksheetw.write(n, 4, categories)
    worksheetw.write(n, 5, str(review))
    worksheetw.write(n, 6, str(rating))
    worksheetw.write(n, 7, price)
    print("|".join([id, name, address, str(zipcode), categories, str(review), str(rating), price]))
    n += 1

workbookw.save("SF.xls")