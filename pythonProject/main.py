from table_actions import (create_tables,
                           add_user, add_post,
                           get_all_posts, get_all_users, get_posts_by_user_id,
                           update_email, update_content,
                           delete_user, delete_post)


if __name__ == '__main__':
    create_tables()

    # add_user("Polina", "polina@gmail.com", "PolinaPassword")
    # add_user("Oleg", "oleg@email.ru", "oleg12345")
    #
    # add_post("Cat", "Look at my cat!!!", 1)
    # add_post("Dog", "I got a dog too", 1)

    # add_post("Hello", "Hello, I am jast an Oleg", 2)

    # update_email(1, "polina_email")
    # update_content(4, "I am Oleg, bye")

    # delete_post(3)

    # delete_user(1)

    users = get_all_users()
    for user in users:
        print(user.id, user.username, user.email, user.password)
    print()

    posts = get_all_posts()
    for post in posts:
        print(post.id, post.title, post.content, post.user_id)
    print()

    posts_by_polina = get_posts_by_user_id(1)
    for post in posts_by_polina:
        print(post.title, post.content, post.user_id)
    print()