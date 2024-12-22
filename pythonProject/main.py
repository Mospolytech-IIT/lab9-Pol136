from table_actions import (create_tables,
                           add_user, add_post,
                           get_all_posts, get_all_users, get_posts_by_user_id,
                           update_email, update_content,
                           delete_user, delete_post)
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

create_tables()

@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    users = get_all_users()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users", response_class=HTMLResponse)
async def create_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    add_user(username, email, password)
    return RedirectResponse("/users", status_code=303)


@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int):
    user = next((u for u in get_all_users() if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})


@app.post("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user(request: Request, user_id: int, email: str = Form(...)):
    try:
        update_email(user_id, email)
        return RedirectResponse("/users", status_code=303)
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/users/{user_id}/delete")
async def delete_user_route(user_id: int):
    try:
        delete_user(user_id)
        return RedirectResponse("/users", status_code=303)
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/posts", response_class=HTMLResponse)
async def read_posts(request: Request):
    posts = get_all_posts()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@app.post("/posts", response_class=HTMLResponse)
async def create_post(request: Request, title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    add_post(title, content, user_id)
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    post = next((p for p in get_all_posts() if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    users = get_all_users()
    return templates.TemplateResponse("post_edit.html", {"request": request, "post": post, "users": users})


@app.post("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, content: str = Form(...)):
    try:
        update_content(post_id, content)
        return RedirectResponse("/posts", status_code=303)
    except:
        raise HTTPException(status_code=404, detail="Post not found")


@app.get("/posts/{post_id}/delete")
async def delete_post_route(post_id: int):
    try:
        delete_post(post_id)
        return RedirectResponse("/posts", status_code=303)
    except:
        raise HTTPException(status_code=404, detail="Post not found")
