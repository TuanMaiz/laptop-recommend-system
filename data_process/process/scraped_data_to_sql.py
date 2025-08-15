import json

with open("data_process/scrape/sazo_laptops.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def escape_sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    if isinstance(value, str):
        return "'" + str(value).replace("'", "''") + "'"
    elif isinstance(value, int) or isinstance(value, float):
        return value


with open("data_process/process/sql_outputs/dml.json", "a", encoding="utf-8") as f:
    for idx, laptop in enumerate(data, 1):
        id = int(idx)
        name = laptop.get("title")
        brand = laptop.get("brand")
        model = None  # Not available in the sample data
        price = laptop.get("price")
        price = int(price.replace("₫", "").replace(",", "").strip()) if price else None
        description = laptop.get("description")
        specifications = laptop.get("specifications")
        image_url = laptop.get("image_url")
        stock_quantity = None  # Not available in the sample data
        category = None  # Not available in the sample data
        processor = specifications.get("CPU") if specifications else None
        ram = specifications.get("Ram") if specifications else None
        storage = specifications.get("Ổ cứng") if specifications else None
        graphics_card = specifications.get("Card màn hình") if specifications else None
        screen_size = specifications.get("Độ phân giải") if specifications else None
        operating_system = (
            specifications.get("Hệ điều hành") if specifications else None
        )
        weight = specifications.get("Trọng lượng") if specifications else None
        weight = (
            float(weight.replace("~", "").replace("kg", "").replace("KG", "").strip())
            if weight
            else None
        )
        battery_life = specifications.get("Pin") if specifications else None

        # sql = f"INSERT INTO laptops (id, name, brand, model, price, description, specifications, image_url, stock_quantity, category, processor, ram, storage, graphics_card, screen_size, operating_system, weight, battery_life)\nVALUES ({escape_sql(id)}, {escape_sql(name)}, {escape_sql(brand)}, {escape_sql(model)}, {escape_sql(price)}, {escape_sql(description)}, {escape_sql(specifications)}, {escape_sql(image_url)}, {escape_sql(stock_quantity)}, {escape_sql(category)}, {escape_sql(processor)}, {escape_sql(ram)}, {escape_sql(storage)}, {escape_sql(graphics_card)}, {escape_sql(screen_size)}, {escape_sql(operating_system)}, {escape_sql(weight)}, {escape_sql(battery_life)});"
        sql = f"INSERT INTO laptops (id, name, brand, model, price, description, specifications, image_url, stock_quantity, category, processor, ram, storage, graphics_card, screen_size, operating_system, weight, battery_life)\nVALUES ({escape_sql(id)}, {escape_sql(name)}, {escape_sql(brand)}, {escape_sql(model)}, {escape_sql(price)}, {escape_sql(description)}, NULL, {escape_sql(image_url)}, {escape_sql(stock_quantity)}, {escape_sql(category)}, {escape_sql(processor)}, {escape_sql(ram)}, {escape_sql(storage)}, {escape_sql(graphics_card)}, {escape_sql(screen_size)}, {escape_sql(operating_system)}, {escape_sql(weight)}, {escape_sql(battery_life)});"
        f.write(sql + "\n")
