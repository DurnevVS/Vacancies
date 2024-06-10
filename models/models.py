from database.types import Column, DataType, Constraint
from database.model import Model
from entities import Company, Vacancy


class Companies(Model):
    company_id = Column(DataType.SERIAL, Constraint.PK)
    name = Column(DataType.VARCHAR)
    url = Column(DataType.VARCHAR)

    entity = Company


class Vacancies(Model):
    vacancy_id = Column(DataType.SERIAL, Constraint.PK)
    name = Column(DataType.VARCHAR)
    company = Column(
        DataType.INTEGER,
        Constraint.FK(
            Companies,
            'company_id'
        )
    )
    salary_from = Column(DataType.INTEGER)
    salary_to = Column(DataType.INTEGER)
    salary_currency = Column(DataType.VARCHAR)
    area = Column(DataType.VARCHAR)
    requirement = Column(DataType.TEXT)
    responsibility = Column(DataType.TEXT)
    url = Column(DataType.TEXT)

    entity = Vacancy

    @classmethod
    def get_companies_and_vacancies_count(cls):
        return {
            company: len(cls.filter(company=company)) for company in Companies.all()
        }

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        vacancies = cls.all()
        return [vacancy for vacancy in vacancies if keyword.strip().lower() in vacancy.name.lower()]

    @classmethod
    def get_avg_salary(cls):
        vacancies = cls.all()
        return sum(
            vacancy._salary.avg_salary for vacancy in vacancies
        ) / len(vacancies)

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        vacancies = cls.all()
        vacancies_with_higher_salary = []
        if vacancies:
            avg = cls.get_avg_salary()
            for vacancy in vacancies:
                if vacancy._salary.avg_salary >= avg:
                    vacancies_with_higher_salary.append(vacancy)

        return vacancies_with_higher_salary
