#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd


# In[34]:


try:
    df = pd.read_csv('vacancies.csv')
except FileNotFoundError:
    df = pd.read_csv('../vacancies.csv')

# A1
# In[17]:


# функция для вычисления описательных статистик для определенного уровня опыта


# In[18]:


# Стратегия с исключением строк с NaN


# In[19]:


def getStatisticsWithOutNaN(df: pd.DataFrame, experience: str) -> pd.DataFrame:
    df_experience = df[df['experience'] == experience]
    df_experience = df_experience.dropna()

    mean_salary = (df_experience['salary_from'] + df_experience['salary_to']) / 2

    return pd.DataFrame({
        'Медиана' : [mean_salary.median()],
        'Среднее' : [mean_salary.mean()],
        'Стандартное отклонение' : [mean_salary.std()],
        '25-й перцентиль' : [mean_salary.quantile(0.25)],
        '75-й перцентиль' : [mean_salary.quantile(0.75)]
    })


# In[20]:


getStatisticsWithOutNaN(df, 'Нет опыта')


# In[21]:


getStatisticsWithOutNaN(df, 'От 1 года до 3 лет')


# In[22]:


getStatisticsWithOutNaN(df, 'От 3 до 6 лет')


# In[23]:


getStatisticsWithOutNaN(df, 'Более 6 лет')


# In[ ]:





# In[24]:


# функция для вычисления описательных статистик для определенного уровня опыта


# In[25]:


''' Если обе границы зарплаты NaN, то заменяем NaN`ы на медианы соответствующих столбцов
    Если только одна из границ - дублируем существующую (тогда получится усреднённое будет то же значение)
'''


# In[26]:


# Замена NaN`ов на медианы на столбцов или на существующие противоположные границы


# In[27]:


def replace_nan_on_median_or_opposite_border(df: pd.DataFrame) -> pd.DataFrame:
    median_salary_from = df['salary_from'].median()
    median_salary_to = df['salary_to'].median()

    # Заполняем salary_from из salary_to (где salary_to не NaN)
    mask = df['salary_from'].isna() & df['salary_to'].notna()
    df.loc[mask, 'salary_from'] = df.loc[mask, 'salary_to']

    # Заполняем salary_to из salary_from (где salary_from не NaN)
    mask = df['salary_to'].isna() & df['salary_from'].notna()
    df.loc[mask, 'salary_to'] = df.loc[mask, 'salary_from']

    # Заполняем оставшиеся NaN медианами
    df['salary_from'] = df['salary_from'].fillna(median_salary_from)
    df['salary_to'] = df['salary_to'].fillna(median_salary_to)

    return df



# In[28]:


def getStatisticsButNaNReplacedMedianAndOpposite_border(df: pd.DataFrame, experience: str) -> pd.DataFrame:
    df_experience = df[df['experience'] == experience]
    df_experience = replace_nan_on_median_or_opposite_border(df_experience)

    mean_salary = (df_experience['salary_from'] + df_experience['salary_to']) / 2

    return pd.DataFrame({
        'Медиана' : [mean_salary.median()],
        'Среднее' : [mean_salary.mean()],
        'Стандартное отклонение' : [mean_salary.std()],
        '25-й перцентиль' : [mean_salary.quantile(0.25)],
        '75-й перцентиль' : [mean_salary.quantile(0.75)]
    })


# In[29]:


getStatisticsButNaNReplacedMedianAndOpposite_border(df, 'Нет опыта')


# In[30]:


getStatisticsButNaNReplacedMedianAndOpposite_border(df, 'От 1 года до 3 лет')


# In[31]:


getStatisticsButNaNReplacedMedianAndOpposite_border(df, 'От 3 до 6 лет')


# In[32]:


getStatisticsButNaNReplacedMedianAndOpposite_border(df, 'Более 6 лет')


# In[ ]:





# In[48]:


# A2. Во всех группах среднее выше медианы. Это указывает на правостороннюю скошенность распределений: относительно небольшое число высоких 
# зарплат «тянет» среднее вверх, тогда как медиана устойчива к таким выбросам.


# In[49]:


# A3. Гистограммы распределения зарплат для каждого уровня опыта


# In[50]:


import matplotlib.pyplot as plt


# In[ ]:





# In[51]:


def getMeanSalaryForExperienceGroup(df: pd.DataFrame, experience):
    df_experience = df[df['experience'] == experience]
    df_experience = df_experience.dropna()

    list_mean_salaries = (df_experience['salary_from'] + df_experience['salary_to']) / 2
    return list_mean_salaries


# In[52]:


fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Гистограмма для 'Нет опыта'
axes[0, 0].hist(getMeanSalaryForExperienceGroup(df, 'Нет опыта'), bins=30, color='green', alpha=0.7)
axes[0, 0].set_title('Нет опыта')
axes[0, 0].set_xlabel('Зарплата(руб.)')
axes[0, 0].set_ylabel('Количество')

# Гистограмма для 'От 1 года до 3 лет'
axes[0, 1].hist(getMeanSalaryForExperienceGroup(df, 'От 1 года до 3 лет'), bins=30, color='blue', alpha=0.7)
axes[0, 1].set_title('От 1 года до 3 лет')
axes[0, 1].set_xlabel('Зарплата(руб.)')
axes[0, 1].set_ylabel('Количество')

# Гистограмма для 'От 3 до 6 лет'
axes[1, 0].hist(getMeanSalaryForExperienceGroup(df, 'От 3 до 6 лет'), bins=30, color='red', alpha=0.7)
axes[1, 0].set_title('От 3 до 6 лет')
axes[1, 0].set_xlabel('Зарплата(руб.)')
axes[1, 0].set_ylabel('Количество')

# Гистограмма для 'Более 6 лет'
axes[1, 1].hist(getMeanSalaryForExperienceGroup(df, 'Более 6 лет'), bins=30, color='black', alpha=0.7)
axes[1, 1].set_title('Более 6 лет')
axes[1, 1].set_xlabel('Зарплата(руб.)')
axes[1, 1].set_ylabel('Количество')

plt.tight_layout()
plt.show()


# In[53]:


# Как видно на графиках выше, наблюдается правосторонняя скошенность распределений для всех выборок по опыту


# In[ ]:





# In[54]:


# Для большей наглядности можно построить ящики с усами, чтобы показат, что распределение в выборках не является норальным


# In[55]:


fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].boxplot(getMeanSalaryForExperienceGroup(df, 'Нет опыта'))
axes[0, 1].boxplot(getMeanSalaryForExperienceGroup(df, 'От 1 года до 3 лет'))
axes[1, 0].boxplot(getMeanSalaryForExperienceGroup(df, 'От 3 до 6 лет'))
axes[1, 1].boxplot(getMeanSalaryForExperienceGroup(df, 'Более 6 лет'))



# In[ ]:




