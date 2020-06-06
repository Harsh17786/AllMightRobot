# Copyright (C) 2018 - 2020 MrYacha.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is part of Sophie.

from sophie.services.mongo import motor_db, mongo_db
from sophie.utils.logging import log

col_name = 'locale'
col_validation = {
    "$jsonSchema":
        {
            "bsonType": "object",
            "required": ["chat_id", "locale_code"],
            "properties": {
                "chat_id": {
                    "bsonType": "int"
                },
                "locale_code": {
                    "bsonType": "string",
                    "pattern": "^[a-z]{2}-[A-Z]{2}$"
                }
            }
        }
}


async def set_lang(chat_id: int, locale_code: str) -> dict:
    data = {
        'chat_id': chat_id,
        'locale_code': locale_code
    }

    await motor_db[col_name].replace_one({'chat_id': chat_id}, data, upsert=True)

    return data


async def get_lang(chat_id: int) -> (str, None):
    data = await motor_db[col_name].find_one({'chat_id': chat_id})
    if not data:
        return None

    return data['locale_code']


def __setup__():
    if col_name not in mongo_db.collection_names():
        log.info(f'Created not exited column "{col_name}"')
        mongo_db.create_collection(col_name)

    log.debug(f'Running validation cmd for "{col_name}" column')
    mongo_db.command({
        'collMod': col_name,
        'validator': col_validation,
        'validationLevel': 'strict'
    })