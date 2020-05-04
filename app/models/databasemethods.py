from datetime import datetime

from sqlalchemy import not_, or_

from .. import db


class DatabaseMethods:
    def to_str(self):
        """Returns the repr of this object."""
        return f'<{type(self).__name__}\n' + '\n'.join(
            f'{field}: {getattr(self, field)}'
            for field in self.get_table_columns()
        ) + '\n>'

    @classmethod
    def get_table_columns(cls):
        if not hasattr(cls, 'table_columns'):
            cls.table_columns = []
            for c in cls.__mro__:
                if hasattr(c, '__table__'):
                    cls.table_columns += [field.name
                                          for field in c.__table__.columns]
            cls.table_columns = list(set(cls.table_columns))
        return cls.table_columns

    @classmethod
    def to_dict(cls, obj, include_fields=None, exclude_fields=None):
        """Return the data as dictionary"""
        if include_fields is None:
            include_fields = cls.get_table_columns()
        if exclude_fields is None:
            exclude_fields = cls.exclude_fields
        return {field: getattr(obj, field)
                for field in include_fields
                if field not in exclude_fields and hasattr(obj, field)}

    @classmethod
    def to_list_of_dict(cls, data_list, include_fields=None,
                        exclude_fields=None):
        """Convert a list of objects to a list of dictionaries"""
        return [cls.to_dict(item, include_fields, exclude_fields)
                for item in data_list]

    def from_dict(self, data_dict, exclude=[]):
        """
        Set the current object attribute from a data_dict. This method does not
        set the excluded fields mentioned in the class declaration.
        :param data_dict:
        :param exclude:
        :return:
        """
        for field in self.get_table_columns():
            if all([field in data_dict, field not in exclude,
                    field not in self.exclude_fields]):
                setattr(self, field, data_dict[field])

    @classmethod
    def has_all_fields(cls, data_dict, exclude_fields=[]):
        """
        Return True if data_dict contains all the required data excluding class
        exclude_fields and exclude_fields passed to the method.
        :param data_dict:
        :param exclude_fields:
        :return:
        """
        if exclude_fields is None:
            exclude_fields = cls.exclude_fields
        return all(
            field.name in data_dict
            for field in cls.get_table_columns()
            if field not in exclude_fields
        )

    @classmethod
    def get_query(cls):
        if hasattr(cls, 'is_archived'):
            return cls.query.filter(not_(cls.is_archived))
        return cls.query

    @classmethod
    def get_by_id(cls, id):
        """
        Get an object by its id. Does not return archived items.
        :param id:
        :return:
        """
        if not hasattr(cls, 'is_archived'):
            return cls.query.get(id)
        return cls.query.filter(not_(cls.is_archived), cls.id == id).first()

    @classmethod
    def text_search(cls, search):
        """
        Search text fields for search term.
        :param search:
        :return:
        """
        query = cls.query
        if hasattr(cls, 'is_archived'):
            query = query.filter(not_(cls.is_archived))
        search_or = [getattr(cls, field).ilike(f'%{search}%')
                     for field in cls.text_fields]
        if search_or:
            query = query.filter(or_(*search_or))
        return query

    @classmethod
    def text_search_with_range(cls, search, start, end):
        query = cls.text_search(search)
        search_count = query.count()
        items_count = cls.get_query().count()
        start, end = max(start, 0), min(end, search_count)
        items = query.slice(start, end)
        return {
            'items_count': items_count,
            'search_count': search_count,
            'start': start,
            'end': end,
            'items': items
        }

    @classmethod
    def can_insert(cls, data_dict):
        """
        Return True if the data can be inserted.
        :param cls:
        :param data_dict:
        :return:
        """
        return all(field in data_dict for field in cls.required_fields)

    @classmethod
    def can_update(cls, data_dict):
        """
        Return True if the data can be updated.
        :param data_dict:
        :return:
        """
        return any(field in data_dict for field in cls.updateable_fields)

    @classmethod
    def prepare_insert(cls, data_dict):
        """
        Creates an object almost ready for insert
        :param cls:
        :param data_dict:
        :return:
        """
        sanitized = {field: data_dict[field]
                     for field in cls.required_fields + cls.optional_fields
                     if field in data_dict}
        return cls(**sanitized)

    def prepare_update(self, data_dict):
        """Prepares this object for a future update"""
        sanitized = {field: data_dict[field]
                     for field in self.updateable_fields
                     if field in data_dict}
        self.from_dict(sanitized)

    def insert(self):
        """Commits insert for this item"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return False
        return True

    def delete(self):
        """Commits delete for this item"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return False
        return True

    @staticmethod
    def update():
        """Commits update for one item"""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def persist_changes(data_dict):
        """
        Persists inserts, updates and deletes at one. The data should be
        sanitized before calling this method.
        :param data_dict: a dictionary with three keys 'insert', 'delete'
        :return:
        """
        try:
            if 'insert' in data_dict:
                db.session.add_all(data_dict['insert'])
            if 'delete' in data_dict:
                for item in data_dict['delete']:
                    db.session.delete(item)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        return True

    def archive(self):
        if not hasattr(self, 'is_archived') or not hasattr(self, 'dt_archive'):
            return False
        self.is_archived = True
        self.dt_archive = datetime.now()
        return self.update()
