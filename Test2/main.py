from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine, text
from langchain.llms import OpenAI
# from langchain_community.llms import OpenAI
# from langchain_community.chat_models import ChatOpenAI

# MySQL connection string
cs = "mysql+pymysql://root@localhost/etl_self_service"

# Create database engine 
db_engine = create_engine(cs)

# Initialize SQLDatabase instance
db = SQLDatabase(db_engine)



# llm = ChatOpenAI(temperature=0.0, model="gpt-4")
llm = OpenAI(temperature=0.7, openai_api_key="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")

# Initialize SQLDatabaseToolkit
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

# Define conversation prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        You are a very intelligent AI assistant who is an expert in identifying relevant questions from users and converting them into SQL queries to generate correct answers.
        Please use the below context to write the MySQL queries.
        Context:
        You must query against the connected database, which has a total of 13 tables: history_order, tb_answer, tb_customer, tb_customer_login, tb_login, tb_menu, tb_package_info, tb_package_main_offer_info, tb_package_matching, tb_package_order, tb_set_user_permission, tb_trouble, tb_user.
        The history_order table has columns ids, package_matching_id, phone, data_time, status, phone_re, which give information about history order package.
        The tb_answer table has columns id, trou_id, text_ans,text_ans_la, list, status, which give information about answer for customer.
        The tb_customer table has columns ids, cus_id, full_name, username,password, which give information about customer.
        The tb_customer_login table has columns id, cus_id, login_date, status, which provide information about time login for customer.
        The tb_login table has columns id, user_id, login_date, status, which give information about time login.
        The tb_menu table has columns id, menu_name, menu_name_la, status, icon, link, which give information about menu for website.
        The tb_package_info has columns ids, package_name, package_offer_id, period_days, free_resource, prices, ussd_register, note, status, date_time_insert , which give information about package.
        The tb_package_main_offer_info has columns ids, main_offer_id, offer_name, note, which give information about type of SIM.
        The tb_package_matching has columns ids, main_offer_id, package_offer_id, date_insert , which give information about matching tb_package_info and tb_package_main_offer_info.
        The tb_package_order has columns id , which give information about order package.
        The tb_set_user_permission has columns id, menu_id, user_id, permission_status , which give information about permission of user login.
        The tb_trouble has columns id, trou_id, trou_name, trou_name_la, status, which give information about trouble of customer.
        The tb_user has coolumns id, full_name, username, password, status, level, note, which give information about customer register.
        As an expert, you must use joins whenever required.
        """
        ),
        ("user", "{question}\nAI: ")
    ]
)


agent = create_sql_agent(llm=llm, toolkit=sql_toolkit, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_execution_time=100, max_iterations=1000)
 
agent.run(prompt.format_prompt(question="How many table  in database"))


# query = text("""
#     SELECT *
#     FROM tb_package_info;
# """)


# with db_engine.connect() as conn:
#     result = conn.execute(query)


# for row in result.fetchall():
#     print(row)
