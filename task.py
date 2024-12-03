from tkinter import Tk, Label, Entry, Button
import requests


window = Tk()
window.title("Task Scheduler")
window.geometry("700x450")

BASE_URL = "http://127.0.0.1:5000/tasks"

Label(window, text="User ID").grid(row=0, column=0, sticky='w', padx=10, pady=9)
ui_entry = Entry(window)
ui_entry.grid(row=0, column=1, padx=10, pady=9)

Label(window, text="Task Name").grid(row=1, column=0, sticky='w', padx=10, pady=9)
tn_entry = Entry(window)
tn_entry.grid(row=1, column=1, padx=10, pady=9)

Label(window, text="End Date").grid(row=2, column=0, sticky='w', padx=10, pady=9)
ed_entry = Entry(window)
ed_entry.grid(row=2, column=1, padx=10, pady=9)

Label(window, text="Task ID").grid(row=3, column=0, sticky='w', padx=10, pady=9)
ti_entry = Entry(window)
ti_entry.grid(row=3, column=1, padx=10, pady=9)

res = Label(window, text="Fetching...", fg="blue", justify="left")
res.grid(row=6, column=0, columnspan=2)

def add_task():
    user_id = ui_entry.get()
    task_name = tn_entry.get()
    end_date = ed_entry.get()
    
    if not user_id or not task_name or not end_date:
        res.config(text="Details mismatch")
        return
    
    data = {
        "user_id": user_id,
        "task_name": task_name,
        "end_date": end_date,
        "completed": None
    }
    
    out = requests.post(BASE_URL, json=data)
    if out.status_code == 200:
        res.config(text="Task added successfully")
    else:
        res.config(text="Error")

def get_task():
    user_id = ui_entry.get()
    
    if not user_id:
        res.config(text="User ID is required")
        return
    
    out = requests.get(BASE_URL, params={"user_id": user_id})
    if out.status_code == 200:
        tasks = out.json().get("tasks", [])
        tasks_text = "\n".join([f"{task.get('task_name')})" for task in tasks])
        res.config(text=f"Tasks:\n{tasks_text}")
    else:
        res.config(text="Error")

def update_task():
    task_id = ti_entry.get()
    user_id = ui_entry.get()
    task_name = tn_entry.get()
    
    if not user_id or not task_name or not task_id:
        res.config(text="Details mismatch")
        return
    
    data = {
        "user_id": user_id,
        "task_name": task_name,
        "completed": None
    }
    
    out = requests.put(f"{BASE_URL}/{task_id}", json=data)
    if out.status_code == 200:
        res.config(text="Task updated successfully")
    else:
        res.config(text="Error")

def delete_task():
    task_id = ti_entry.get()
    if not task_id:
        res.config(text="Task ID is required")
        return
    
    out = requests.delete(f"{BASE_URL}/{task_id}")
    if out.status_code == 200:
        res.config(text="Task deleted successfully")
    else:
        res.config(text="Error")

Button(window, text="Add Task", command=add_task).grid(row=4, column=0, sticky='w', padx=10, pady=9)
Button(window, text="Get Tasks", command=get_task).grid(row=4, column=1, sticky='w', padx=10, pady=9)
Button(window, text="Update Task", command=update_task).grid(row=5, column=0, sticky='w', padx=10, pady=9)
Button(window, text="Delete Task", command=delete_task).grid(row=5, column=1, sticky='w', padx=10, pady=9)

window.mainloop()