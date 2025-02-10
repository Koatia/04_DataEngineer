import pandas as pd
import matplotlib.pyplot as plt

# Загрузка датасета
file_path = 'train.csv'  # Укажите путь к вашему файлу
df = pd.read_csv(file_path)
#%%
# 1. Обработка пропущенных значений
# Определение пропусков
missing_values = df.isnull().sum()
columns_to_drop = missing_values[missing_values > len(df) * 0.5].index.tolist()
df_cleaned = df.drop(columns=columns_to_drop)

# Заполнение пропусков для числовых столбцов медианой
num_cols_with_na = df_cleaned.select_dtypes(include=["float64", "int64"]).columns
df_cleaned[num_cols_with_na] = df_cleaned[num_cols_with_na].fillna(df_cleaned[num_cols_with_na].median())

# Заполнение пропусков для категориальных столбцов модой
cat_cols_with_na = df_cleaned.select_dtypes(include=["object"]).columns
df_cleaned[cat_cols_with_na] = df_cleaned[cat_cols_with_na].fillna(df_cleaned[cat_cols_with_na].mode().iloc[0])

# Проверка дубликатов
df_cleaned = df_cleaned.drop_duplicates()
#%%
# 2. Разведочный анализ данных
# Распределение целевой переменной
plt.figure(figsize=(10, 6))
plt.hist(df_cleaned['SalePrice'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribution of SalePrice', fontsize=16)
plt.xlabel('SalePrice', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
#%%
# Корреляция с SalePrice
# Выбираем только числовые столбцы для вычисления корреляционной матрицы
numerical_features = df_cleaned.select_dtypes(include=['int64', 'float64'])
correlation_matrix = numerical_features.corr()
saleprice_correlation = correlation_matrix['SalePrice'].sort_values(ascending=False)

# Топ-5 коррелирующих признаков
top_features = ['OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea', 'TotalBsmtSF']
for feature in top_features:
    plt.figure(figsize=(8, 6))
    plt.scatter(df_cleaned[feature], df_cleaned['SalePrice'], alpha=0.7, edgecolor='k')
    plt.title(f'SalePrice vs {feature}', fontsize=16)
    plt.xlabel(feature, fontsize=12)
    plt.ylabel('SalePrice', fontsize=12)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.show()
#%%
# 3. Проектирование признаков
# One-hot encoding для категориальных переменных
df_encoded = pd.get_dummies(df_cleaned, drop_first=True)

# Создание новых характеристик
df_encoded['TotalSF'] = df_encoded['TotalBsmtSF'] + df_encoded['1stFlrSF'] + df_encoded['2ndFlrSF']
df_encoded['HouseAge'] = df_encoded['YrSold'] - df_encoded['YearBuilt']
#%%
# Сохранение очищенного датасета
output_path = 'cleaned_house_prices.csv'
df_encoded.to_csv(output_path, index=False)

print(f"Очищенный и преобразованный файл сохранен в: {output_path}")