import os
import pandas as pd


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        files_with_price = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if 'price' in file.lower():
                    files_with_price.append(os.path.join(root, file))

        for file in files_with_price:
            try:
                csv_data = pd.read_csv(file)
                title, price, weigth = None
                for col in csv_data.columns:
                    if col.lower() in ['товар', 'название', 'наименование', 'продукт']:
                        # print(col)
                        title = col
                    elif col.lower() in ['розница', 'цена']:
                        price = col
                        # print(col)
                    elif col.lower() in ['вес', 'масса', 'фасовка']:
                        weigth = col
                        # print(col)
                if title and price and weigth:
                    print(title, price, weigth)
                    data = csv_data[[title, price, weigth]].values.tolist()
                    self.data.extend(data)
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''

        pass

    def export_to_html(self, fname='output.html'):
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
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

    def find_text(self, text):
        """Ищет товар по фрагменту названия и возвращает результаты с сортировкой по цене за килограмм."""
        results = []
        for item in self.data:
            if fragment.lower() in item[0].lower():
                results.append(item)
        sorted_results = sorted(results, key=lambda x: x[3])  # Сортировка по цене за килограмм
        return sorted_results


pm = PriceMachine()
pm.load_prices(os.getcwd())
print(pm.data)

# print('the end')
# print(pm.export_to_html())
while True:
    fragment = input("Введите фрагмент названия товара для поиска (или 'exit' для выхода): ")
    if fragment.lower() == 'exit':
        print("Программа завершена.")
        break
    results = pm.find_text(fragment)
    if results:
        print("Результаты поиска:")
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Товар: {result[0]}, Цена: {result[1]}, Вес: {result[2]}, Цена за кг: {result[3]}")
    else:
        print("Ничего не найдено.")