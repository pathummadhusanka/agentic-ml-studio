from ollama import chat

def generate_response(prompt):
	response = chat(
		model="llama3",
		messages=[
			{
				"role": "user",
				"content" : prompt
			}
		]
	)

	return response.message.content