import openai

# Set up your OpenAI API key
openai.api_key = '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'

def generate_follow_up_question(input_query):
    # Constructing the prompt for ChatGPT
    prompt = f"Pretend I am a person who does not have robust technology literacy and does not know how to make specific and well defined search queries. I look up {input_query}. What is the most important follow up question you might need to ask me in order to get a more specific and well defined search query? For the follow up question, I want it to be very simple, specific, easy to answer with a 2-4 categorical answers that are provided in square brackets [(a),(b),(c),...)] and ALWAYS an other option as the last option, but the other option also needs to have a letter in front of it and should be structured the same way as all the other options. I do not want it to be a compound question. I want it to be just ONE simple question not multiple."

    # Generate response from ChatGPT
    response = openai.completions.create( 
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens=256,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extracting the follow-up questions from the response
    follow_up_questions = response.choices[0].text.strip()

    return follow_up_questions

def prompt_user(question):
    # Prompting the user to answer the follow-up question
    user_answer = input(f"{question} ")
    return user_answer

def refine_query(user_input, user_answer, follow_up_question):
    # Generate a more specific version of the original query
    prompt = f"Pretend I am a person who does not have robust technology literacy and does not know how to make specific and well defined search queries. I look up {user_input}. This is a pretty broad and not well defined search query. My friend asks me the question {follow_up_question}. I give the exact response {user_answer}. Given my response to this question and my original query, come up with a more specific version of my query that better represents my search needs that is a few (1-3) words longer than the original input. The additions to the query should be related only to my answer to the specific question and should not include any additional keywords that are not related to the question."
    response = openai.completions.create( 
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens=256,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    specific_query = response.choices[0].text.strip()
    return specific_query

def get_multiple_choice(user_input):
        # Find the index of the first '[' and the index of the last ']'
    start_index = user_input.find('[')
    end_index = user_input.rfind(']')
    
    # Extract the choices substring
    choices_str = user_input[start_index + 1:end_index]
    
    # Split the choices string by commas
    choices_list = choices_str.split(',')
    
    # Strip leading and trailing whitespace from each choice
    choices_list = [choice.strip() for choice in choices_list]
    
    return choices_list


# Take input from the user
user_input = input("Enter your query: ")

while True:
    # Generate follow-up question based on the initial input query
    follow_up_question = generate_follow_up_question(user_input)

    # Prompt the user to answer the follow-up question
    user_answer = prompt_user(follow_up_question)

    # Generate a more specific query based on the user's answer
    user_input = refine_query(user_input, user_answer, follow_up_question)

    # Output the specific query
    print("Specific query based on your answer:", user_input)

    # Ask for another follow-up question or break the loop
    continue_choice = input("Do you want to ask another follow-up question? (yes/no): ")
    if continue_choice.lower() != 'yes':
        break

