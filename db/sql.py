import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from math import ceil

load_dotenv()


# * Connection
def _create_connection():
    """
    Connects to the MySQL database using environment variables.
    Returns:
        connection: MySQL connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return connection
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None


# * Cards list
def get_all_cards(include_alternative=True):
    """
    Fetches all cards with full descriptive data by replacing foreign key IDs with their names.
    """
    connection = _create_connection()
    if not connection:
        return []

    alt_filter = "" if include_alternative else "WHERE alternative = 0"

    query = f"""
        SELECT
            c.id,
            c.card_number,
            c.name,
            ct.name AS card_type,
            r.name AS rarity,
            co1.name AS color_one,
            co2.name AS color_two,
            co3.name AS color_three,
            c.image_url,
            c.cost,
            s.name AS stage,
            a.name AS attribute,
            t1.name AS type_one,
            t2.name AS type_two,
            bt.abbreviation AS bt_abbreviation,
            c.alternative
        FROM Cards c
        LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
        LEFT JOIN Rarities r ON r.id = c.rarity_id
        LEFT JOIN Colors co1 ON co1.id = c.color_one_id
        LEFT JOIN Colors co2 ON co2.id = c.color_two_id
        LEFT JOIN Colors co3 ON co3.id = c.color_three_id
        LEFT JOIN Stages s ON s.id = c.stage_id
        LEFT JOIN Attributes a ON a.id = c.attribute_id
        LEFT JOIN Types t1 ON t1.id = c.type_one_id
        LEFT JOIN Types t2 ON t2.id = c.type_two_id
        LEFT JOIN BTs bt ON bt.id = c.bt_id
        {alt_filter}
        ORDER BY c.name ASC
    """

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_cards_with_ids(include_alternative: bool = True) -> list[dict]:
    """
    Fetches all cards with full descriptive data, returning the IDs of foreign keys instead of names.
    
    Args:
        include_alternative (bool): If False, excludes alternative cards (alternative = 1).
    
    Returns:
        List of dictionaries, each representing a card with IDs for foreign keys.
    """
    connection = _create_connection()
    if not connection:
        return []

    alt_filter = "" if include_alternative else "WHERE c.alternative = 0"

    query = f"""
        SELECT
            c.id,
            c.card_number,
            c.name,
            c.card_type_id AS card_type,
            c.rarity_id AS rarity,
            c.color_one_id AS color_one,
            c.color_two_id AS color_two,
            c.color_three_id AS color_three,
            c.image_url,
            c.cost,
            c.stage_id AS stage,
            c.attribute_id AS attribute,
            c.type_one_id AS type_one,
            c.type_two_id AS type_two,
            c.bt_id AS bt_abbreviation,
            c.alternative
        FROM Cards c
        {alt_filter}
        ORDER BY c.name ASC
    """

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        cards = cursor.fetchall()
        return cards
    except Exception as e:
        print(f"Error al obtener cartas: {e}")
        return []
    finally:
        connection.close()


def get_all_cards_full_info(include_alternative=True):
    """
    Fetches all cards with full descriptive data by replacing foreign key IDs with their names.
    """
    connection = _create_connection()
    if not connection:
        return []

    alt_filter = "" if include_alternative else "WHERE alternative = 0"

    query = f"""
        SELECT
            c.id,
            c.card_number,
            c.name,
            c.dp,
            ct.name AS card_type,
            r.name AS rarity,
            co1.name AS color_one,
            co2.name AS color_two,
            co3.name AS color_three,
            c.image_url,
            c.cost,
            s.name AS stage,
            a.name AS attribute,
            t1.name AS type_one,
            t2.name AS type_two,
            c.evolution_cost_one,
            c.evolution_cost_two,
            c.effect,
            c.evolution_effect,
            c.security_effect,
            bt.abbreviation AS bt_abbreviation,
            c.alternative
        FROM Cards c
        LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
        LEFT JOIN Rarities r ON r.id = c.rarity_id
        LEFT JOIN Colors co1 ON co1.id = c.color_one_id
        LEFT JOIN Colors co2 ON co2.id = c.color_two_id
        LEFT JOIN Colors co3 ON co3.id = c.color_three_id
        LEFT JOIN Stages s ON s.id = c.stage_id
        LEFT JOIN Attributes a ON a.id = c.attribute_id
        LEFT JOIN Types t1 ON t1.id = c.type_one_id
        LEFT JOIN Types t2 ON t2.id = c.type_two_id
        LEFT JOIN BTs bt ON bt.id = c.bt_id
        {alt_filter}
        ORDER BY c.name ASC
    """

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()



def get_single_card_by_card_number(card_number):
    """
    Fetches a single main card (non-alternative) by its card_number.
    """
    connection = _create_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                c.id,
                c.card_number,
                c.name,
                c.dp,
                ct.name AS card_type,
                r.name AS rarity,
                co1.name AS color_one,
                co2.name AS color_two,
                co3.name AS color_three,
                c.image_url,
                c.cost,
                s.name AS stage,
                a.name AS attribute,
                t1.name AS type_one,
                t2.name AS type_two,
                c.evolution_cost_one,
                c.evolution_cost_two,
                c.effect,
                c.evolution_effect,
                c.security_effect,
                bt.abbreviation AS bt_abbreviation,
                c.alternative
            FROM Cards c
            LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
            LEFT JOIN Rarities r ON r.id = c.rarity_id
            LEFT JOIN Colors co1 ON co1.id = c.color_one_id
            LEFT JOIN Colors co2 ON co2.id = c.color_two_id
            LEFT JOIN Colors co3 ON co3.id = c.color_three_id
            LEFT JOIN Stages s ON s.id = c.stage_id
            LEFT JOIN Attributes a ON a.id = c.attribute_id
            LEFT JOIN Types t1 ON t1.id = c.type_one_id
            LEFT JOIN Types t2 ON t2.id = c.type_two_id
            LEFT JOIN BTs bt ON bt.id = c.bt_id
            WHERE c.card_number = %s AND c.alternative = 0
            LIMIT 1
        """
        cursor.execute(query, (card_number,))
        return cursor.fetchone()

    finally:
        connection.close()


def get_card_with_alternatives_by_card_number(card_number):
    """
    Fetches a single card and its alternative versions.
    """
    connection = _create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        # Obtener la carta principal exacta
        query = """
            SELECT
                c.id,
                c.card_number,
                c.name,
                c.dp,
                ct.name AS card_type,
                r.name AS rarity,
                co1.name AS color_one,
                co2.name AS color_two,
                co3.name AS color_three,
                c.image_url,
                c.cost,
                s.name AS stage,
                a.name AS attribute,
                t1.name AS type_one,
                t2.name AS type_two,
                c.evolution_cost_one,
                c.evolution_cost_two,
                c.effect,
                c.evolution_effect,
                c.security_effect,
                bt.abbreviation AS bt_abbreviation,
                c.alternative
            FROM Cards c
            LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
            LEFT JOIN Rarities r ON r.id = c.rarity_id
            LEFT JOIN Colors co1 ON co1.id = c.color_one_id
            LEFT JOIN Colors co2 ON co2.id = c.color_two_id
            LEFT JOIN Colors co3 ON co3.id = c.color_three_id
            LEFT JOIN Stages s ON s.id = c.stage_id
            LEFT JOIN Attributes a ON a.id = c.attribute_id
            LEFT JOIN Types t1 ON t1.id = c.type_one_id
            LEFT JOIN Types t2 ON t2.id = c.type_two_id
            LEFT JOIN BTs bt ON bt.id = c.bt_id
            WHERE c.card_number = %s AND c.alternative = 0
            LIMIT 1
        """
        cursor.execute(query, (card_number,))
        main_card = cursor.fetchone()

        if not main_card:
            return []

        # Buscar alternativas con card_number que empieza igual y sufijo '_%'
        alt_pattern = card_number + "_%"
        query = """
            SELECT id, card_number
            FROM Cards
            WHERE card_number LIKE %s AND alternative = 1
        """
        cursor.execute(query, (alt_pattern,))
        alt_cards = cursor.fetchall()

        return [main_card] + alt_cards

    finally:
        connection.close()


def search_cards_by_name(name_part):
    """ Searches all main cards (non-alternative) whose names contain the given substring. 
    
    Args: name_part (str): Substring to search for in card names. 
    
    Returns: list[dict]: List of matching cards.
    """
    connection = _create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                c.id,
                c.card_number,
                c.name,
                c.dp,
                ct.name AS card_type,
                r.name AS rarity,
                co1.name AS color_one,
                co2.name AS color_two,
                co3.name AS color_three,
                c.image_url,
                c.cost,
                s.name AS stage,
                a.name AS attribute,
                t1.name AS type_one,
                t2.name AS type_two,
                c.evolution_cost_one,
                c.evolution_cost_two,
                c.effect,
                c.evolution_effect,
                c.security_effect,
                bt.abbreviation AS bt_abbreviation,
                c.alternative
            FROM Cards c
            LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
            LEFT JOIN Rarities r ON r.id = c.rarity_id
            LEFT JOIN Colors co1 ON co1.id = c.color_one_id
            LEFT JOIN Colors co2 ON co2.id = c.color_two_id
            LEFT JOIN Colors co3 ON co3.id = c.color_three_id
            LEFT JOIN Stages s ON s.id = c.stage_id
            LEFT JOIN Attributes a ON a.id = c.attribute_id
            LEFT JOIN Types t1 ON t1.id = c.type_one_id
            LEFT JOIN Types t2 ON t2.id = c.type_two_id
            LEFT JOIN BTs bt ON bt.id = c.bt_id
            WHERE c.name LIKE %s AND c.alternative = 0
            ORDER BY c.name ASC
        """

        search_term = f"%{name_part}%"
        cursor.execute(query, (search_term,))
        return cursor.fetchall()

    finally:
        connection.close()


def search_cards_with_alternatives_by_name(name_part):
    """ 
    Searches all main cards (non-alternative) whose names contain the given substring, and includes their alternative versions, all in a single query. 
    
    Args: name_part (str): Substring to search for in card names. 
    
    Returns: list[dict]: List of main cards, each with an 'alternatives' key containing a list of its alternative versions.
    """
    connection = _create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        search_term = f"%{name_part}%"
        query = """
            SELECT
                main.id AS main_id,
                main.card_number AS main_card_number,
                main.name AS main_name,
                main.dp AS main_dp,
                ct_main.name AS main_card_type,
                r_main.name AS main_rarity,
                co1_main.name AS main_color_one,
                co2_main.name AS main_color_two,
                co3_main.name AS main_color_three,
                main.image_url AS main_image_url,
                main.cost AS main_cost,
                s_main.name AS main_stage,
                a_main.name AS main_attribute,
                t1_main.name AS main_type_one,
                t2_main.name AS main_type_two,
                main.evolution_cost_one AS main_evolution_cost_one,
                main.evolution_cost_two AS main_evolution_cost_two,
                main.effect AS main_effect,
                main.evolution_effect AS main_evolution_effect,
                main.security_effect AS main_security_effect,
                bt_main.abbreviation AS main_bt_abbreviation,

                alt.id AS alt_id,
                alt.card_number AS alt_card_number,
                alt.name AS alt_name,
                alt.image_url AS alt_image_url,
                alt.alternative AS alt_alternative
            FROM Cards main
            LEFT JOIN Cards alt ON alt.card_number LIKE CONCAT(main.card_number, '_%') AND alt.alternative = 1
            LEFT JOIN CardTypes ct_main ON ct_main.id = main.card_type_id
            LEFT JOIN Rarities r_main ON r_main.id = main.rarity_id
            LEFT JOIN Colors co1_main ON co1_main.id = main.color_one_id
            LEFT JOIN Colors co2_main ON co2_main.id = main.color_two_id
            LEFT JOIN Colors co3_main ON co3_main.id = main.color_three_id
            LEFT JOIN Stages s_main ON s_main.id = main.stage_id
            LEFT JOIN Attributes a_main ON a_main.id = main.attribute_id
            LEFT JOIN Types t1_main ON t1_main.id = main.type_one_id
            LEFT JOIN Types t2_main ON t2_main.id = main.type_two_id
            LEFT JOIN BTs bt_main ON bt_main.id = main.bt_id
            WHERE main.name LIKE %s AND main.alternative = 0
            ORDER BY main.name ASC, alt.name ASC
        """
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()

        grouped = {}
        for row in rows:
            key = row["main_card_number"]
            if key not in grouped:
                grouped[key] = {
                    "id": row["main_id"],
                    "card_number": row["main_card_number"],
                    "name": row["main_name"],
                    "dp": row["main_dp"],
                    "card_type": row["main_card_type"],
                    "rarity": row["main_rarity"],
                    "color_one": row["main_color_one"],
                    "color_two": row["main_color_two"],
                    "color_three": row["main_color_three"],
                    "image_url": row["main_image_url"],
                    "cost": row["main_cost"],
                    "stage": row["main_stage"],
                    "attribute": row["main_attribute"],
                    "type_one": row["main_type_one"],
                    "type_two": row["main_type_two"],
                    "evolution_cost_one": row["main_evolution_cost_one"],
                    "evolution_cost_two": row["main_evolution_cost_two"],
                    "effect": row["main_effect"],
                    "evolution_effect": row["main_evolution_effect"],
                    "security_effect": row["main_security_effect"],
                    "bt_abbreviation": row["main_bt_abbreviation"],
                    "alternatives": [],
                }

            if row["alt_id"]:
                grouped[key]["alternatives"].append(
                    {
                        "id": row["alt_id"],
                        "card_number": row["alt_card_number"],
                        "name": row["alt_name"],
                        "image_url": row["alt_image_url"],
                        "alternative": row["alt_alternative"],
                    }
                )

        return list(grouped.values())

    finally:
        connection.close()


# * Auxiliary tables get all
def get_all_bts():
    """
    Retrieves all BT sets from the database.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM BTs"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_colors():
    """
    Retrieves all color options.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Colors"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_card_types():
    """
    Retrieves all card types.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM CardTypes"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_rarities():
    """
    Retrieves all rarity types.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Rarities"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_stages():
    """
    Retrieves all evolution stages.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Stages"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_attributes():
    """
    Retrieves all attributes.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Attributes"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_all_types():
    """
    Retrieves all types.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Types"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


# * Auxiliary tables get one
def get_bt_by_id(bt_id):
    """
    Retrieves a BT entry by ID.

    Args:
        bt_id (int): ID of the BT.

    Returns:
        dict or None: BT record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM BTs WHERE id = %s"
        cursor.execute(query, (bt_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_color_by_id(color_id):
    """
    Retrieves a Color entry by ID.

    Args:
        color_id (int): ID of the Color.

    Returns:
        dict or None: Color record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Colors WHERE id = %s"
        cursor.execute(query, (color_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_card_type_by_id(card_type_id):
    """
    Retrieves a Card Type by ID.

    Args:
        card_type_id (int): ID of the Card Type.

    Returns:
        dict or None: CardType record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM CardTypes WHERE id = %s"
        cursor.execute(query, (card_type_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_rarity_by_id(rarity_id):
    """
    Retrieves a Rarity by ID.

    Args:
        rarity_id (int): ID of the Rarity.

    Returns:
        dict or None: Rarity record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Rarities WHERE id = %s"
        cursor.execute(query, (rarity_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_stage_by_id(stage_id):
    """
    Retrieves a Stage by ID.

    Args:
        stage_id (int): ID of the Stage.

    Returns:
        dict or None: Stage record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Stages WHERE id = %s"
        cursor.execute(query, (stage_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_attribute_by_id(attribute_id):
    """
    Retrieves an Attribute by ID.

    Args:
        attribute_id (int): ID of the Attribute.

    Returns:
        dict or None: Attribute record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Attributes WHERE id = %s"
        cursor.execute(query, (attribute_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_type_by_id(type_id):
    """
    Retrieves a Type by ID.

    Args:
        type_id (int): ID of the Type.

    Returns:
        dict or None: Type record or None if not found.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Types WHERE id = %s"
        cursor.execute(query, (type_id,))
        return cursor.fetchone()
    finally:
        connection.close()


# * Collection
def get_collection(page=1, per_page=25, include_alternative=True):
    """
    Fetches cards from the collection with full descriptive data by replacing foreign key IDs with their names,
    including the quantity of each card in the collection.
    Supports pagination.

    Args:
        page (int): Page number to fetch.
        per_page (int): Number of cards per page (10, 25, 50).
        include_alternative (bool): Whether to include alternative artwork cards (default: True)

    Returns:
        list[dict]: List of card records with full information and quantity.
    """
    connection = _create_connection()
    if not connection:
        return []

    offset = (page - 1) * per_page
    alt_filter = "" if include_alternative else "AND c.alternative = 0"

    query = f"""
        SELECT
            c.id,
            c.card_number,
            c.name,
            ct.name AS card_type,
            r.name AS rarity,
            co1.name AS color_one,
            co2.name AS color_two,
            co3.name AS color_three,
            c.image_url,
            c.cost,
            s.name AS stage,
            a.name AS attribute,
            t1.name AS type_one,
            t2.name AS type_two,
            bt.abbreviation AS bt_abbreviation,
            c.alternative,
            col.quantity
        FROM Collection col
        JOIN Cards c ON c.card_number = col.card_number
        LEFT JOIN CardTypes ct ON ct.id = c.card_type_id
        LEFT JOIN Rarities r ON r.id = c.rarity_id
        LEFT JOIN Colors co1 ON co1.id = c.color_one_id
        LEFT JOIN Colors co2 ON co2.id = c.color_two_id
        LEFT JOIN Colors co3 ON co3.id = c.color_three_id
        LEFT JOIN Stages s ON s.id = c.stage_id
        LEFT JOIN Attributes a ON a.id = c.attribute_id
        LEFT JOIN Types t1 ON t1.id = c.type_one_id
        LEFT JOIN Types t2 ON t2.id = c.type_two_id
        LEFT JOIN BTs bt ON bt.id = c.bt_id
        WHERE 1=1 {alt_filter}
        LIMIT %s OFFSET %s
    """

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (per_page, offset))
        return cursor.fetchall()
    finally:
        connection.close()


def add_card_to_collection(card_number, quantity=1):
    """
    Adds a new card to the collection or increases quantity if it already exists.

    Args:
        card_number (str): Card number to add.
        quantity (int): Quantity to add (default is 1).

    Returns:
        bool: True if inserted or updated, False if failed.
    """
    connection = _create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO Collection (card_number, quantity)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """
        cursor.execute(query, (card_number, quantity))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_card_from_collection(card_number):
    """
    Deletes a card from the collection by its card number.

    Args:
        card_number (str): Card number to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    connection = _create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            DELETE FROM Collection
            WHERE card_number = %s
        """
        cursor.execute(query, (card_number,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def update_card_in_collection(card_number: str, new_quantity: int):
    """
    Updates the quantity of a card in the collection.
    If the new quantity is 0 or less, the card is removed from the collection.

    Args:
        card_number (str): Card number to update
        new_quantity (int): New quantity for the card

    Returns:
        tuple: (success: bool, action: str)
               success: True if operation was successful
               action: 'updated', 'removed', or 'not_found'
    """
    connection = _create_connection()
    if not connection:
        return (False, "connection_error")

    try:
        cursor = connection.cursor()

        if new_quantity <= 0:
            # Remove the card completely if quantity is 0 or less
            query = """
                DELETE FROM Collection
                WHERE card_number = %s
            """
            cursor.execute(query, (card_number,))
            action = "removed"
        else:
            # Update to the new quantity
            query = """
                UPDATE Collection
                SET quantity = %s
                WHERE card_number = %s
            """
            cursor.execute(query, (new_quantity, card_number))
            action = "updated"

        connection.commit()

        if cursor.rowcount == 0:
            return (False, "not_found")

        return (True, action)

    except Exception as e:
        connection.rollback()
        print(f"Error updating card in collection: {e}")
        return (False, "error")
    finally:
        connection.close()


# * Decks
def get_all_decks():
    """
    Fetches all existing decks.

    Returns:
        list[dict]: List of decks.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Decks"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_deck_cards(deck_id):
    """
    Retrieves all cards and their quantities from a given deck.

    Args:
        deck_id (int): Deck ID to fetch cards for.

    Returns:
        list[dict]: List of cards with quantity and name/image.
    """
    connection = _create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT dc.card_number, c.name, dc.quantity, c.image_url
            FROM DeckCards dc
            JOIN Cards c ON dc.card_number = c.card_number
            WHERE dc.deck_id = %s
        """
        cursor.execute(query, (deck_id,))
        return cursor.fetchall()
    finally:
        connection.close()


def create_deck(name, color_id=None, image=None):
    """
    Creates a new deck with optional color and image.

    Args:
        name (str): Name of the deck.
        color_id (int, optional): Color ID.
        image (str, optional): Image URL or path.

    Returns:
        int: ID of the newly created deck.
    """
    connection = _create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Decks (name, color_id, image) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, color_id, image))
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def add_card_to_deck(deck_id, card_number, quantity):
    """
    Adds a card to a deck. If it exists, sets the quantity to the new value.

    Args:
        deck_id (int): Deck ID.
        card_number (str): Card number.
        quantity (int): Quantity to set.

    Returns:
        bool: True on success.
    """
    connection = _create_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO DeckCards (deck_id, card_number, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = VALUES(quantity)
        """
        cursor.execute(query, (deck_id, card_number, quantity))
        connection.commit()
        return True
    finally:
        connection.close()


def update_card_in_deck(deck_id, card_number, quantity):
    """
    Sets the quantity of a specific card in a deck.
    If quantity is 0, the card is removed from the deck.

    Args:
        deck_id (int): Deck ID.
        card_number (str): Card number.
        quantity (int): New quantity.

    Returns:
        bool: True if updated or deleted, False otherwise.
    """
    connection = _create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        if quantity == 0:
            # Delete the card from the deck
            query = """
                DELETE FROM DeckCards
                WHERE deck_id = %s AND card_number = %s
            """
            cursor.execute(query, (deck_id, card_number))
        else:
            # Update the quantity
            query = """
                UPDATE DeckCards
                SET quantity = %s
                WHERE deck_id = %s AND card_number = %s
            """
            cursor.execute(query, (quantity, deck_id, card_number))

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_card_from_deck(deck_id, card_number):
    """
    Deletes a specific card from a deck entirely.

    Args:
        deck_id (int): Deck ID.
        card_number (str): Card number to remove.

    Returns:
        bool: True if the card was deleted, False otherwise.
    """
    connection = _create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            DELETE FROM DeckCards
            WHERE deck_id = %s AND card_number = %s
        """
        cursor.execute(query, (deck_id, card_number))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()
