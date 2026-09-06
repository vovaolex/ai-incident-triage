import requests

# response = requests.get(
#     "https://jsonplaceholder.typicode.com/todos?userId=1"
# )
params = {
    "userId": 1
}

response = requests.get(
    "https://jsonplaceholder.typicode.com/todos",
    params=params
)

print(f"Status code: {response.status_code}")

if response.status_code == 200:
    todos = response.json()

    print(f"Total todos: {len(todos)}")

    for todo in todos[:5]:
        print(todo["id"], "-", todo["title"])

else:
    print("API request failed")




#print(response.status_code)
#print(response.json())