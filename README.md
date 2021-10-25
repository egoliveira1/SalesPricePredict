# SalesPriceProduct
Project to help a new company define the **selling price for men's pants** in the American market.



![Screenshot](https://github.com/egoliveira1/SalesPricePredict/blob/main/img/cover_img_edit.png)



## 1. Business problem:

Eduardo and Marcelo are two Brazilians, friends, and partners in a venture. After several successful businesses, they are planning to enter the US fashion market with an e-commerce business model called **Star Jeans**.

The initial idea is to enter the market with **only one product and for a specific audience**, in this case, the product will be **jeans for men**.  The goal is to keep the cost of operation low and scale up as they get customers.

However, even with the entrance product and the audience defined, the two partners have no experience in this fashion market and therefore do not know how to **define** basic things like **price**, the **model** of the pants, and the **material** to manufacture each piece.

So, the two partners hired a Data Science consultancy to answer the following questions:

1. **What is the best sales price for the pants?**
2. **How many types of pants and their colors for the initial product?**
3. **What raw materials are needed to make the pants?**

Start Jeans' main competitors are the American companies **H&M** and **Macy's**.



## 2. Planning the solution:

#### Business Issues: 

1. **What is the best sales price for the pants?**
2. **How many types of pants and their colors for the initial product?**
3. **What raw materials are needed to make the pants?**



#### Steps:

##### Outputs: (Final Product)

1. Answers to the questions
   - Median of product values from competitors' websites.
2. Delivery format
  - Table or graph

3. Delivery location
  - Streamlit App

##### Processes: (Actions)

1. Response: 
   - Perform the median calculation
2. Format: 
    - Elaborate the bar chart 
    - Build the table with the following features: 
       id | product_id | product_name | product_model | product_color | product_composition | product_price
    - Define schema: Columns and their types
    - Define the storage infrastructure (SQLITE3)
    - Build the ETL (Data Extraction, Transformation and Load) design
    - Plan the script scheduling (dependencies)
    - Make the visualizations
    - Deliver the final product


3. Delivery location:
   - App with Streamlit

##### Inputs:

1. Data sources:
	- H&M Website: https://www2.hm.com/en_us/men/products/jeans.html
	- Macy's Website: https://www.macys.com/shop/mens-clothing/mens-jeans
2. Tools
	- Python 3.8.0
	- Webscrapping libraries (BS4, Selenium)
	- JupyterLab (Analysis, prototyping and coding)
	- Cron job, Airflow
	- Streamlit



## 3. Running the solution:

#### First stage - Exploration, and extraction

The project started with an exploratory analysis of the H&M website, to get to know the structure of the HTML and locate where the information the project needs is. The products are distributed in two ways on the website, there is a first layer, which I called "Showcase", where are the products listed by model, and when accessing each model there are subdivisions by color. It is important to inform that the composition of each pant depends on the model and color, so it is necessary to extract the data individually.

Knowing the structure and the data tags, I programmed a first version of the code that extracted the URL of each product from the showcase. Then, with the product codes in a column of the data frame, it was possible to enter each model and get the complete data of color, composition, style, model, price, and size.



![Screenshot](https://github.com/egoliveira1/SalesPricePredict/blob/main/img/ETL_design.png)



#### Second Stage - Cleaning and Transformation

The next step was cleaning and transforming the data. Using Regex tools, and data manipulation with Pandas, it was possible to remove "dirt", separate information, and organize the data.

This step resulted in a Dataset with all the products separated by ID, color, name, price, and composition. The table has the final format for the calculations planned for the delivery of the final product.

#### Third Stage - Automation and Loading

In the third stage of the project, I organized the automatic execution of the scrip to perform daily data extractions and load the data into SQLITE3. The process will take 30 days, and then the product will be built and delivered to the company. 

The project solution was validated in a prototype built-in Google Sheets.



![Screenshot](https://github.com/egoliveira1/SalesPricePredict/blob/main/img/dashboard_prototype.png)



## 4. Next steps:

The next steps of the project foresee the following actions:

- Adapt the code to extract the information from Macy's website;
- Use Airflow to automate the execution of the collection jobs on both sites (H&M and Macy's);
- Build the App in Streamlit;
- Perform the first delivery of the solution;
- Evaluate the need for a second development cycle.



## 5. Lessons Learned:

Companies are in permanent improvement of their products. Therefore, new features may emerge that did not exist when in the first version of code. Care must be taken so that the solution can handle the emergence of new information.









