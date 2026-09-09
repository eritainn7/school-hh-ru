#!/usr/bin/env python
# coding: utf-8

# In[28]:


from py.block_a import *


# In[29]:


def getSkewness(df: pd.DataFrame, experience: str):
    df_exp = df[df['experience'] == experience]
    df_exp = df_exp.dropna()

    mean_salary = (df_exp["salary_to"] + df_exp['salary_from']) / 2

    return mean_salary.skew()



# In[30]:


skewness_beginner = getSkewness(df, 'Нет опыта')
skewness_beginner


# In[31]:


skewness_1_3_year = getSkewness(df, 'От 1 года до 3 лет')
skewness_1_3_year


# In[32]:


skewness_3_6_year = getSkewness(df, 'От 3 до 6 лет')
skewness_3_6_year


# In[33]:


skewness_more_6_year = getSkewness(df, 'Более 6 лет')
skewness_more_6_year


# In[34]:


# B1. Наибольший коэффициент асимметрии у группы <от 1 года до 3 лет>.
# Это может объясняться ошибками парсинга, выбросами, значения которых сильно выше для типичных этой группы.
# Хвост распределения тянется вправо(правосторонняя ассиметрия), так как существуют аномально большие значения
# Так же аномальные значения возможны из-за неверной интерпретации валют, географии рабочего места.


# In[35]:


# B2. среднее арифметическое чувствительно к каждому значению, включая экстремальные выбросы, а медиана — нет.
# Медиана — это значение, которое делит выборку пополам, и на неё влияют только значения в середине упорядоченного ряда.
''' Когда распределение скошено вправо (положительная асимметрия), основная масса значений сосредоточена на 
относительно низких зарплатах, но есть небольшой «хвост» из очень высоких зарплат '''

# Чем выше коэффициент асимметрии, тем сильнее расхождение среднего и медианы


# In[ ]:





# In[36]:


def getRangeMetrics(df: pd.DataFrame, experience: str):
    df_exp = df[df['experience'] == experience]
    df_exp = df_exp.dropna()

    mean_salary = (df_exp["salary_to"] + df_exp['salary_from']) / 2

    metrics = [
        mean_salary.std(),  # стандартное отклонение
        mean_salary.quantile(0.75) - mean_salary.quantile(0.25), # межквартильный размах
        mean_salary.std() / mean_salary.mean() # коэффициент вариации
    ]

    return metrics


# In[37]:


getRangeMetrics(df, 'Нет опыта')


# In[38]:


getRangeMetrics(df, 'От 1 года до 3 лет')


# In[39]:


getRangeMetrics(df, 'От 3 до 6 лет')


# In[40]:


getRangeMetrics(df, 'Более 6 лет')


# In[41]:


# Данные сильно искажены выбросами, CV > 1 указывает на то, что стандартное отклонение больше среднего. Такое возможно только при наличии экстремальных выбросов.
# Напишем функцию для фильтрации от аномалий


# In[42]:


# Подготовка данных: расчёт точечной зарплаты
import numpy as np
def calculate_salary(row):
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    if pd.notna(salary_from) and pd.notna(salary_to):
        if salary_from <= salary_to:
            return (salary_from + salary_to) / 2
        else:
            return (salary_to + salary_from) / 2
    elif pd.notna(salary_from):
        return salary_from
    elif pd.notna(salary_to):
        return salary_to
    else:
        return np.nan


# In[43]:


df['salary'] = df.apply(calculate_salary, axis=1)
df = df.dropna(subset=['salary'])


# In[44]:


# Очистка от аномалий (ключевой шаг!)
LOW_SALARY = 10**4
HIGH_SALARY = 10**6
df_clean = df[(df['salary'] >= LOW_SALARY) & (df['salary'] <= HIGH_SALARY)]


# In[45]:


# Функция расчёта метрик разброса
def getRangeMetrics(df: pd.DataFrame, experience: str):
    df_exp = df[df['experience'] == experience].dropna(subset=['salary'])

    if df_exp.empty:
        return [float('nan'), float('nan'), float('nan')]

    salary = df_exp['salary']
    std_dev = salary.std()
    iqr = salary.quantile(0.75) - salary.quantile(0.25)
    cv = std_dev / salary.mean() if salary.mean() != 0 else float('nan')

    return [std_dev, iqr, cv]


# In[46]:


# Проверяем на очищенных данных
metrics = getRangeMetrics(df_clean, 'Нет опыта')
print(f"std: {metrics[0]:.0f}")
print(f"IQR: {metrics[1]:.0f}")
print(f"CV: {metrics[2]:.2f}")


# In[47]:


metrics = getRangeMetrics(df_clean, 'От 1 года до 3 лет')
print(f"std: {metrics[0]:.0f}")
print(f"IQR: {metrics[1]:.0f}")
print(f"CV: {metrics[2]:.2f}")


# In[48]:


metrics = getRangeMetrics(df_clean, 'От 3 до 6 лет')
print(f"std: {metrics[0]:.0f}")
print(f"IQR: {metrics[1]:.0f}")
print(f"CV: {metrics[2]:.2f}")


# In[49]:


metrics = getRangeMetrics(df_clean, 'Более 6 лет')
print(f"std: {metrics[0]:.0f}")
print(f"IQR: {metrics[1]:.0f}")
print(f"CV: {metrics[2]:.2f}")


# In[50]:


# B3. Наибольший относительный разброс для группы <От 1 года до 3 лет> (CV = 0.62) — зарплаты очень неоднородны.
# Это самая неопределённая группа для прогнозирования. При медиане 150.000 реальные предложения могут варьироваться от 60.000 до 300.000
'''
   Чтобы снизить неопределённость, необходимо анализировать зарплаты отдельно по городам типу занятости и др.
   Это сузит диапазон и сделает прогноз точнее.
   Для группы 1–3 года IQR = 97 500.
'''
getStatisticsWithOutNaN(df_clean, 'От 1 года до 3 лет') #207500 - 110000


# In[51]:


# Это значит, что 50% предложений лежат в диапазоне примерно 110000.0 - 207500.0
# Cтоит ориентироваться на верхнюю границу этого диапазона, если есть конкурентные преимущества (опыт работы, знание инструментов, хорошее портфолио)


# In[ ]:




