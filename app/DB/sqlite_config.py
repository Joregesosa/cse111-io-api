import sqlite3

script = """
            DROP TABLE IF EXISTS `users`;
            CREATE TABLE `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT NOT NULL,
                `email` TEXT NOT NULL,
                `password` TEXT NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            DROP TABLE IF EXISTS `categories`;
            CREATE TABLE `categories` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT NOT NULL,
                `user_id` INTEGER NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            );

            DROP TABLE IF EXISTS `expenses`;
            CREATE TABLE `expenses` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `user_id` INTEGER NOT NULL,
                `category_id` INTEGER NOT NULL,
                `amount` DECIMAL(10,0) NOT NULL,
                `description` TEXT NOT NULL,
                `r_balance` DECIMAL(10,0) NOT NULL,
                `expense_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            );

            DROP TABLE IF EXISTS `incomes`;
            CREATE TABLE `incomes` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `user_id` INTEGER,
                `amount` DECIMAL(10,0) NOT NULL,
                `description` TEXT,
                `r_balance` DECIMAL(10,0) NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            );

            DROP TABLE IF EXISTS `balances`;
            CREATE TABLE `balances` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `user_id` INTEGER NOT NULL,
                `amount` DECIMAL(10,0) NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
            );

            DROP TRIGGER IF EXISTS `after_insert_incomes`;
            CREATE TRIGGER `after_insert_incomes` AFTER INSERT ON `incomes`
            BEGIN
                UPDATE balances SET amount = amount + NEW.amount WHERE user_id = NEW.user_id;
            END;

            DROP TRIGGER IF EXISTS `after_insert_expenses`;
            CREATE TRIGGER `after_insert_expenses` AFTER INSERT ON `expenses`
            BEGIN
                UPDATE balances SET amount = amount - NEW.amount WHERE user_id = NEW.user_id;
            END;

            DROP TRIGGER IF EXISTS `after_update_expenses`;
            CREATE TRIGGER `after_update_expenses` AFTER UPDATE ON `expenses`
            BEGIN
                UPDATE balances SET amount = amount + OLD.amount - NEW.amount WHERE user_id = NEW.user_id;
            END;

            DROP TRIGGER IF EXISTS `after_update_incomes`;
            CREATE TRIGGER `after_update_incomes` AFTER UPDATE ON `incomes`
            BEGIN
                UPDATE balances SET amount = amount - OLD.amount + NEW.amount WHERE user_id = NEW.user_id;
            END;
            
            DROP TRIGGER IF EXISTS `after_insert_users`;
            CREATE TRIGGER `after_insert_users` AFTER INSERT ON `users`
            BEGIN
                INSERT INTO balances (user_id, amount) VALUES (NEW.id, 0);
            END;
    """


def create_database():
    try:
        conn = sqlite3.connect("app/DB/io_db.sqlite")
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        print("Database created successfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()


create_database()
