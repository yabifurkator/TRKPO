from model import model


def make_user(user_id: int) -> model.User:
    return model.User(telegramID=str(user_id))


def list_entries(entry_list: list[model.Entry], user_id: int):
    user_entries: list[model.Entry] = []

    for entry in entry_list:
        if entry.user.telegramID == str(user_id):
            user_entries.append(entry)

    return user_entries
