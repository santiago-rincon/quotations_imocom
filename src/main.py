from docxtpl import DocxTemplate
from datetime import datetime
import flet as ft
import locale
locale.setlocale(locale.LC_ALL, '')


def main(page: ft.Page):

    ##### Functions #####
    def validate_number(e):
        field = e.control
        if (not field.value.isdigit()) and len(field.value) > 0:
            page.open(ft.SnackBar(
                ft.Text("⚠ Solo se permiten números"), duration=3000))
            field.value = field.value[:-1]
            page.update()

    def save_doc(e: ft.FilePickerResultEvent):
        # TODO check data before create document
        try:
            page.remove(error_text)
        except:
            pass
        try:
            doc = DocxTemplate('./assets/schema.docx')  # production path
            # doc = DocxTemplate('src/assets/schema.docx')  # development path
            products = []
            total_send = 0
            f_time = ""
            if quotation_type_field.value == quotations_types["IMPORT"]:
                title_header = "Ítem"
                f_time = f"Se estima un plazo de entrega de {final_time.value.lower()} semanas, tiempos estimados una vez confirmada su orden de \t\t\tcompra y el anticipo"
            elif quotation_type_field.value == quotations_types["STOCK"]:
                title_header = "Código de artículo"
                f_time = "Stock, salvo venta previa"
            for row in table_info.rows:
                product = {
                    'item': row.cells[0].content.value,
                    'description': row.cells[1].content.value,
                    'send_date': row.cells[2].content.value,
                    'quantity': row.cells[3].content.value,
                    'unit': row.cells[4].content.value,
                    'selling_price': row.cells[5].content.value,
                    'amount': row.cells[6].content.value
                }
                total_send += int(product['selling_price'].replace('.',
                                  '').replace('$ ', ''))*int(product['quantity'])
                products.append(product)
            total = total_send
            taxes = total*0.19
            rounded = round((total + taxes) % 1, 3)
            if rounded >= 0.5:
                rounded = round(1 - rounded, 3)
            else:
                rounded = rounded*(-1)
            final_price = total + taxes + rounded
            context = {'client': client_field.value,
                       'cv': cv_field.value,
                       'date': current_date,
                       'contact': contact_field.value,
                       'address': address_field.value,
                       'location': location_field.value,
                       'title_header': title_header,
                       'products': products,
                       'currency': currency_field.value,
                       'total_send': locale.currency(
                           total_send, grouping=True),
                       'total': locale.currency(total, grouping=True),
                       'taxes': locale.currency(taxes, grouping=True),
                       'rounded': rounded,
                       'final_price': locale.currency(final_price, grouping=True),
                       'pay_type': pay_type.value,
                       'currency_text': currencies[currency_field.value],
                       'contact_imocom': imocom_contact.value,
                       'job_title': job_title.value,
                       'final_time': f_time
                       }
            doc.render(context)
            doc.save(e.path + ".docx")
            banner.content.value = f"El archivo de cotización se creó exitosamente en: {e.path}.docx"
            page.open(banner)
        except Exception as E:
            error_text.value = E
            page.add(error_text)
            page.update()
            print(E)

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.icons.LIGHT_MODE_OUTLINED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.icons.NIGHTLIGHT_OUTLINED
        page.update()

    def add_product(e):
        product = []
        if quotation_type_field.value == quotations_types["IMPORT"]:
            id = str(len(table_info.rows)+1)
        elif quotation_type_field.value == quotations_types["STOCK"]:
            id = article_code_field.value.upper()
        product.append(id)
        description = description_field.value
        quantity = int(quantity_field.value)
        unit = unit_field.value
        try:
            if len(description) > 0 and len(str(quantity)) > 0 and len(unit) > 0:
                product.append(description)
                product.append(current_date)
                product.append(quantity)
                product.append(unit)
                product.append(locale.currency(
                    int(selling_price.value), grouping=True).replace(',00', ''))
                product.append(locale.currency(
                    int(quantity*int(selling_price.value)), grouping=True).replace(',00', ''))
            else:
                raise Exception('')
        except:
            page.open(ft.SnackBar(
                ft.Text("⚠ Todos los campos son obligatorios"), duration=3000))
            return
        table_info.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(product[0], selectable=True)),
                ft.DataCell(ft.Text(product[1], selectable=True)),
                ft.DataCell(ft.Text(product[2], selectable=True)),
                ft.DataCell(ft.Text(product[3], selectable=True)),
                ft.DataCell(ft.Text(product[4], selectable=True)),
                ft.DataCell(ft.Text(product[5], selectable=True)),
                ft.DataCell(ft.Text(product[6], selectable=True)),
                ft.DataCell(ft.Row(controls=[ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                    icon_color="red400",
                    icon_size=20,
                    tooltip="Eliminar producto",
                    on_click=delete_product,
                    key=id
                )],
                    alignment=ft.MainAxisAlignment.CENTER))
            ])
        )
        description_field.value = ""
        quantity_field.value = ""
        unit_field.value = ""
        selling_price.value = ""
        article_code_field.value = ""
        page.update()

    def delete_product(e):
        deleted = False
        for row in table_info.rows.copy():
            if row.cells[7].content.controls[0].key == e.control.key and not deleted:
                table_info.rows.remove(row)
                deleted = True
                continue
            if deleted:
                row.cells[0].content.value = int(
                    row.cells[0].content.value) - 1
        page.update()

    def close_banner(e):
        page.close(banner)

    def handle_quotation_type_aux(e):
        handle_quotation_type()

    def handle_quotation_type():
        quotation_type = quotation_type_field.value
        table_info.rows.clear()
        if quotation_type == quotations_types["IMPORT"]:
            pay_type.options = [
                ft.dropdownm2.Option(
                    "50 % Anticipo para iniciar el proceso de importación, 50% 30 días fecha factura"),
                ft.dropdownm2.Option(
                    "50 % Anticipo para iniciar el proceso de importación, 50% contraentrega"),
                ft.dropdownm2.Option("100% Anticipado"),
            ]
            table_row.controls = [description_field, quantity_field, unit_field, selling_price,
                                  add_btn]
            table_info.columns[0].label.value = "Item"
            other_data_row.controls = [pay_type, final_time, currency_field]
        elif quotation_type == quotations_types["STOCK"]:
            pay_type.options = [
                ft.dropdownm2.Option("Contado"),
                ft.dropdownm2.Option("30 diás factura"),
            ]
            table_row.controls = [article_code_field, description_field, quantity_field, unit_field, selling_price,
                                  add_btn]
            table_info.columns[0].label.value = "Código del artículo"
            other_data_row.controls = [pay_type, currency_field]
        page.update(table_row, table_info_row, pay_type, other_data_row)

    def clear_fileds(e):
        client_field.value = ""
        contact_field.value = ""
        cv_field.value = ""
        address_field.value = ""
        location_field.value = ""
        quotation_type_field.value = quotations_types["IMPORT"]
        article_code_field.value = ""
        description_field.value = ""
        quantity_field.value = ""
        unit_field.value = ""
        selling_price.value = ""
        pay_type.value = ""
        final_time.value = ""
        currency_field.value = ""
        imocom_contact.value = ""
        job_title.value = ""
        handle_quotation_type()
        page.update()
    ##### Global Variables #####
    padding = 25
    current_date = datetime.today().strftime("%d/%m/%Y")
    currencies = {
        'USD': 'Dólares Americanos + IVA liquidados a la TRM del día de facturación',
        'COP': 'Pesos Colombianos + IVA',
        'EUR': 'Euros + IVA liquidados a la TRM del día de facturación'
    }
    quotations_types = {
        'IMPORT': 'Repuestos de importación',
        'STOCK': 'Repuestos en stock'
    }

    ##### Page #####
    page.scroll = ft.ScrollMode.AUTO
    page.title = "Cotizaciones Imocom"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = padding
    page.spacing = 20

    ##### Header #####
    text_header = ft.Text("Cotizaciones Imocom Mecanizado",
                          size=30, weight=ft.FontWeight.BOLD)
    theme_toggle = ft.IconButton(
        icon=(ft.icons.NIGHTLIGHT_OUTLINED if page.theme_mode ==
              ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE_OUTLINED),
        icon_color="blue400",
        icon_size=20,
        tooltip="Cambiar apariencia",
        on_click=change_theme
    )
    header = ft.Row([text_header, theme_toggle],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    ##### Client info #####
    client_info = ft.Row(controls=[ft.Text("Información del cliente", size=20, weight=ft.FontWeight.BOLD)],
                         alignment=ft.MainAxisAlignment.CENTER)
    client_field = ft.TextField(
        label="Cliente", hint_text="Ingresa el nombre del cliente", expand=2)
    contact_field = ft.TextField(
        label="Contacto del cliente", hint_text="Sra. Angela Cruz", expand=2)
    cv_field = ft.TextField(
        label="Número de CV", prefix_text="CV-", on_change=validate_number, expand=1)
    address_field = ft.TextField(
        label="Dirección", hint_text="Parque industrial San Jorge, Bodega 10", expand=1)
    location_field = ft.TextField(
        label="Ubicación", hint_text="Mosquera, Cundinamarca", expand=1)
    quotation_type_field = ft.DropdownM2(
        options=[
            ft.dropdownm2.Option(quotations_types["IMPORT"]),
            ft.dropdownm2.Option(quotations_types["STOCK"]),
        ],
        expand=1,
        hint_text="Seleccione el tipo de cotización",
        on_change=handle_quotation_type_aux,
        value=quotations_types["IMPORT"]
    )
    row1 = ft.Row(controls=[client_field, contact_field,  cv_field],
                  spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    row2 = ft.Row(controls=[address_field, location_field, quotation_type_field],
                  spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    ##### Product info #####
    product_title = ft.Row(controls=[ft.Text("Información del producto", size=20, weight=ft.FontWeight.BOLD)],
                           alignment=ft.MainAxisAlignment.CENTER)
    article_code_field = ft.TextField(
        label="Código del artículo", hint_text="G111000001", expand=1)
    description_field = ft.TextField(
        label="Descripción", hint_text="Descripción del item", expand=4)
    quantity_field = ft.TextField(
        label="Cantidad", hint_text="1", expand=1, on_change=validate_number)
    unit_field = ft.TextField(
        label="Unidad", hint_text="UND", expand=1)
    selling_price = ft.TextField(
        label="Precio de venta", prefix_text="$", expand=1, on_change=validate_number)
    add_btn = ft.IconButton(
        icon=ft.Icons.ADD,
        icon_color="green400",
        icon_size=27,
        tooltip="Añadir producto",
        on_click=add_product
    )
    table_row = ft.Row(controls=[description_field, quantity_field, unit_field, selling_price,
                                 add_btn],
                       spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ##### Table info product #####
    table_info = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Item"), numeric=True),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Fecha de envío")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Unidad")),
            ft.DataColumn(ft.Text("Precio de venta")),
            ft.DataColumn(ft.Text("Importe")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        width=0.9*page.width,
        data_row_min_height=48,
        data_row_max_height=float('inf'),
    )
    table_info_row = ft.Row(
        controls=[table_info], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    ##### Other data #####
    other_data_title = ft.Row(controls=[ft.Text("Otros datos", size=20, weight=ft.FontWeight.BOLD)],
                              alignment=ft.MainAxisAlignment.CENTER)
    pay_type = ft.DropdownM2(
        options=[
            ft.dropdownm2.Option(
                "50 % Anticipo para iniciar el proceso de importación, 50% 30 días fecha factura"),
            ft.dropdownm2.Option(
                "50 % Anticipo para iniciar el proceso de importación, 50% contraentrega"),
            ft.dropdownm2.Option("100% Anticipado"),
        ],
        expand=2,
        hint_text="Seleccione la forma de pago",
    )
    final_time = ft.TextField(
        label="Tiempo de entrega en semanas", hint_text="6 a 7", expand=1)
    currency_field = ft.DropdownM2(
        options=[
            ft.dropdownm2.Option("USD"),
            ft.dropdownm2.Option("COP"),
            ft.dropdownm2.Option("EUR"),
        ],
        expand=1,
        hint_text="Seleccione la moneda",
    )
    imocom_contact = ft.TextField(
        label="Contacto de Imocom", hint_text="Ingresa el nombre del contacto de Imocom", expand=1)
    job_title = ft.TextField(
        label="Puesto de trabajo", hint_text="Ingresa el puesto de trabajo", expand=1)
    other_data_row = ft.Row(controls=[
                            pay_type, final_time, currency_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    other_data_row2 = ft.Row(controls=[imocom_contact,
                                       job_title], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    ##### Buttons #####
    save_btn = ft.FilePicker(on_result=save_doc)
    page.overlay.append(save_btn)
    send_button = ft.Row(controls=[ft.OutlinedButton(content=ft.Text("Generar cotización", size=18), on_click=lambda _: save_btn.save_file(
        file_type=ft.FilePickerFileType.CUSTOM, file_name=f"CV-{cv_field.value}-{client_field.value}", allowed_extensions=["docx"]))], alignment=ft.MainAxisAlignment.START, expand=1)
    clear_button = ft.Row(controls=[ft.OutlinedButton(
        content=ft.Text("Limpiar campos", size=18), on_click=clear_fileds)], alignment=ft.MainAxisAlignment.END, expand=1)
    buttons_row = ft.Row(
        controls=[send_button, clear_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    ##### Banner #####
    action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)
    banner = ft.Banner(
        bgcolor=ft.Colors.GREEN_100,
        leading=ft.Icon(ft.Icons.CHECK_CIRCLE_SHARP,
                        color=ft.Colors.GREEN, size=40),
        content=ft.Text(
            value="",
            color=ft.Colors.BLACK,
        ),
        actions=[
            ft.TextButton(text="Ok", style=action_button_style,
                          on_click=close_banner)
        ],
    )

    ##### Debug info #####
    error_text = ft.Text("Error:", color=ft.colors.RED)

    ##### Footer #####
    footer = ft.Container(content=ft.Row(controls=[ft.Text("© Desarrollado por: Cristian Santiago Rincón, 2025 Imocom", color="#95979e", weight=ft.FontWeight.BOLD)],
                                         alignment=ft.MainAxisAlignment.CENTER), expand=1, alignment=ft.alignment.bottom_center)

    page.add(header, client_info, row1, row2, product_title, table_row, table_info_row,
             other_data_title, other_data_row, other_data_row2, buttons_row, footer)


ft.app(main)
