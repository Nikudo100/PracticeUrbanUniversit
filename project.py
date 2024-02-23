# pip install pyarrow pandas
import os
import pandas as pd


class PriceMachine():
    def __init__(self):
        self.data = []

    def load_prices(self, directory='.'):
        """Загружает данные из всех прайс-листов в указанной папке."""
        files_with_price = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if 'price' in file.lower():
                    files_with_price.append(os.path.join(root, file))

        for file in files_with_price:
            file_name = os.path.basename(file)
            try:
                csv_data = pd.read_csv(file)
                product_col, price_col, weight_col = None, None, None
                for col in csv_data.columns:
                    if col.lower() in ['товар', 'название', 'наименование', 'продукт']:
                        product_col = col
                    elif col.lower() in ['розница', 'цена']:
                        price_col = col
                    elif col.lower() in ['вес', 'масса', 'фасовка']:
                        weight_col = col
                if all([product_col, price_col, weight_col]):
                    csv_data[price_col] = csv_data[price_col].astype(int)
                    csv_data[weight_col] = csv_data[weight_col].astype(int)
                    csv_data['price_per_kg'] = round(csv_data[price_col] / csv_data[weight_col], 2)
                    csv_data['file'] = file_name
                    data = csv_data[[product_col, price_col, weight_col, 'price_per_kg', 'file']]
                    self.data.extend(data.values.tolist())
            except Exception as e:
                print(f"Ошибка чтения файла {file}: {str(e)}")

        self.data = sorted(self.data, key=lambda x: x[3])

    def find_text(self, fragment):
        """Ищет товар по фрагменту названия и возвращает результаты с сортировкой по цене за килограмм."""
        results = []
        for item in self.data:
            if fragment.lower() in item[0].lower():
                # print(item)/
                results.append(item)
        sorted_results = sorted(results, key=lambda x: x[3])
        return sorted_results


    def export_to_html(self, fname='output.html'):
        """ Создавем html из собранных данных """
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Цена за кг.</th>
                    <th>Файл</th>
                </tr>
        '''
        for i, item in enumerate(self.data, start=1):
            tr = '''
            <tr>
                <td> {} </td>
                <td> {} </td>
                <td> {} </td>
                <td> {} </td>
                <td> {} </td>
                <td> {} </td>
            </tr>
            '''.format(i, *item)
            result += tr

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

pm = PriceMachine()
pm.load_prices(os.getcwd())
pm.export_to_html()
while True:
    fragment = input("Введите фрагмент названия товара для поиска (или 'exit' для выхода): ")
    if fragment.lower() == 'exit':
        print("Программа завершена.")
        break
    results = pm.find_text(fragment)
    if results:
        print("Результаты поиска:")
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Товар: {result[0]}, Цена: {result[1]}, Вес: {result[2]}, Цена за кг: {result[3]}, Файл: {result[4]}")
    else:
        print("Ничего не найдено.")
