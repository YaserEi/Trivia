import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
      # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={r'/*/api/*': {'origins': '*'}})





  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access_Control_Allow_Headers', 'Content-Type, Authorization, True')
        response.headers.add('Access_control_Allow_Methods', "GET, POST, PATCH, DELETE, OPTIONS")

        return response

      # '''
      # @TODO:
      # Create an endpoint to handle GET requests
      # for all available categories.
      # '''
    @app.route('/categories')
    def categories():
        cats=Category.query.all()
        formated_cat = [cat.format() for cat in cats]
        return jsonify({
          'success': True,
          'categories': formated_cat
          })

      # @TODO:
      # Create an endpoint to handle GET requests for questions,
      # including pagination (every 10 questions).
      # This endpoint should return a list of questions,
      # number of total questions, current category, categories.

    @app.route('/questions')
    def questions():
        page = request.args.get('page',1,type=int)
        start = (page-1) *10
        end = start +10
        all_categories=[]
        categories = Category.query.all()
        formated_categories = [category.format() for category in categories]
        questions = Question.query.all()
        formated_questions = [question.format() for question in questions]
        totalQuestions = len(formated_questions)
        for i in range(len(categories)):
            all_categories.append(formated_categories[i]['type'])
        return jsonify({
        'success': True,
        'questions': formated_questions[start:end],
        'totalQuestions': totalQuestions,
        'categories': all_categories,
        # 'currentCategory':
        })
  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.
  # @TODO:
  # Create an endpoint to DELETE question using a question ID.

    @app.route('/questions/<id>', methods=['DELETE'])
    def delete(id):
       question = Question.query.filter_by(id = id).first()
       try:
          db.session.delete(question)
          db.session.commit()
       except:
          print('error')
          db.session.rollback()
       finally:
          db.session.close()
          return jsonify({
          'success': True
          })

  # @TODO:
  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.
    @app.route('/questions', methods = ['POST'])
    def add_question():
        body=request.get_json()
        question = body['question']
        answer = body['answer']
        difficulty = body['difficulty']
        category = body['category']

        add_question = Question(question = question, answer = answer, difficulty = difficulty, category = category)

        try:
            db.session.add(add_question)
            db.session.commit()
        except:
            print('error')
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({ "success":True})

  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.
    @app.route('/questionSearch', methods=['POST'])
    def search():
        body = request.get_json()
        search_result = Question.query.filter(Question.question.ilike('%'+body['searchTerm']+'%')).all()
        total_questions = Question.query.all()
        formated_result = [result.format() for result in search_result]
        print(formated_result)
        return jsonify({
          'success':True,
          'questions': formated_result,
          'totalQuestions': len(total_questions)
          #'currentCategory': categories
        })
  #
  # '''
  # @TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.
    @app.route('/categories/<int:id>/questions', methods = ['GET'])
    def filter_questions(id):
        questions = Question.query.filter_by(category = id).all()
        formated_questions = [question.format() for question in questions]
        return jsonify({
        'success': True,
        'totalQuestions': len(questions),
        'questions': formated_questions
        })
  # @TODO:
  # Create a GET endpoint to get questions based on category.
  #
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  # '''
  #
  #
  # '''
  # @TODO:
  # Create a POST endpoint to get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.
  #
  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.
  # '''
  #
  # '''
  # @TODO:
  # Create error handlers for all expected errors
  # including 404 and 422.
  # '''



    return app
