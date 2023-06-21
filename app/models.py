from mongoengine import *


class Paper(Document):
    id = IntField(primary_key=True)
    doi = StringField(required=True, unique=True)
    extended_doi = StringField()
    title = StringField()
    year = IntField()
    authors = ListField(StringField())
    affiliations = ListField(StringField())
    countries = ListField(ReferenceField('Country'))
    venue = StringField()
    award = StringField()
    certificate = StringField()
    verified = BooleanField(default=False)

    def __repr__(self):
        return f"<Paper {self.doi}>"


class Country(Document):
    name = StringField(primary_key=True)
    code = StringField(max_length=2)

    def __repr__(self):
        return f'<{self.name} ({self.code})>'
    
# class Paper(Document):
#     doi = URLField(primary_key=True)
#     title = StringField(required=True)
#     year = IntField(min_value=1990, required=True)
#     authors = ListField(ReferenceField('Author'))
#     venue = ReferenceField('Venue', required=True)
#     keywords = ListField(StringField(max_length=50))
#     award = ReferenceField('Award', required=True)
#     certificate = FileField()


# class Author(Document):
#     id = UUIDField(primary_key=True)
#     orcid = StringField(max_length=19)
#     first_name = StringField(max_length=50, required=True)
#     last_name = StringField(max_length=50, required=True)
#     institution = ReferenceField('Institution', required=True, unique_with=['first_name', 'last_name'])


# class Institution(Document):
#     name = StringField(primary_key=True)
#     city = StringField()
#     country = StringField()


# class Venue(Document):
#     name = StringField(primary_key=True)
#     acronym = StringField(max_length=50)


# class Award(Document):
#     name = StringField(primary_key=True)


