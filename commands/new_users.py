import config
from models import Session, User
from utils import bot, bot_id, logger, get_user


def ban_bots(message):
    """Scans new members for bots,
    if there are user bots among new users -- kicks the bots
    and adds the rest of the users to the database
    """

    # If the members were invited by an admin, skips the bot detection
    admin_invited = message.from_user.id in config.admin_ids

    session = Session()

    # Checks every new member
    for member in message.new_chat_members:
        # If new member is bot, kicks it out and moves on
        if member.is_bot and member.id != bot_id and not admin_invited:
            bot.kick_chat_member(chat_id=config.chat_id, user_id=member.id)
            logger.info("Bot {} has been kicked out".format(get_user(member)))
            continue

        # If new member has joined for the first time
        # adds him/her to the database
        if not session.query(User).get(member.id):
            user_obj = User(member.id)
            session.add(user_obj)
            logger.info(
                "User {} has joined the chat for the first time and "
                "has been successfully added to the database".format(get_user(member))
            )

    session.commit()
    session.close()


def restrict(message):
    """
    Forbid new users from sending inline bot spam.
    """
    session = Session()

    for new_member in message.new_chat_members:
        member = session.query(User).filter(User.user_id == new_member.id).one_or_none()

        # Skip restriction if user already have messages.
        if member is not None and member.msg_count >= 10:
            continue

        bot.restrict_chat_member(
            chat_id=config.chat_id,
            user_id=new_member.id,
            can_send_other_messages=False,
            can_send_messages=True,
            can_send_media_messages=True,
            can_add_web_page_previews=True,
        )

    session.close()
