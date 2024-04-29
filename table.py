import xlsxwriter
from data import db_session
from data.problem import Problem


def create_table_problem(status=False):
    workbook = xlsxwriter.Workbook('temp/problems.xlsx')
    worksheet = workbook.add_worksheet()

    db_session.global_init("db/applications.db")
    db_sess = db_session.create_session()
    data = db_sess.query(Problem).filter(Problem.status==status).all()
    for row, p in enumerate(data):

        worksheet.write(row, 0, p.id)
        worksheet.write(row, 1, p.fio)
        worksheet.write(row, 2, p.adress)
        worksheet.write(row, 3, p.content)
        worksheet.write(row, 4, p.created_date)
        worksheet.write(row, 5, "Активно" if not p.status else "Закрыто")

    workbook.close()

if __name__ == "__main__":
    create_table_problem()