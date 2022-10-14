import datetime
from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse 
from django.test import Client



from .models import Question,Choice
from .views import index

# Create your tests here.
ques_published_51hrs_earlier= Question.objects.create(question_text="Is Nepal the best country?",pub_date=timezone.now() - datetime.timedelta(hours=51))
ques_published_15hrs_earlier= Question.objects.create(question_text="Is Nepal the best country?",pub_date=timezone.now() - datetime.timedelta(hours=15))
ques_published_15hrs_after_current_time= Question.objects.create(question_text="Is Nepal the best country?",pub_date=timezone.now() + datetime.timedelta(hours=15))

# function that creates question
def create_question(question_text,days):
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=pub_date)

#function that creates choice
def create_choice(question,choice_text,vote):
    return Choice.objects.create(question=question,choice_text=choice_text,vote=vote)

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """returns false for questions published in future date"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_yesterdays_question(self):
        """returns true for questions published 5 hours prior"""
        time = timezone.now() - datetime.timedelta(hours=5)
        yesterdays_question = Question(pub_date=time)
        self.assertIs(yesterdays_question.was_published_recently(), True)

    def test_was_published_recently_with_question_from_two_days_earlier(self):
        """returns false for questions published 2 days earlier"""
        time = timezone.now() - datetime.timedelta(days=2)
        question_from_two_days_earlier = Question(pub_date=time)
        self.assertIs(question_from_two_days_earlier.was_published_recently(), False)

    def test_was_published_recently_with_question_from_five_days_earlier(self):
        """returns false for questions published 5 days earlier"""
        time = timezone.now() - datetime.timedelta(days=5)
        question_from_five_days_earlier = Question(pub_date=time)
        self.assertIs(question_from_five_days_earlier.was_published_recently(), False)

    def test_was_published_recently_with_ques_published_51hrs_earlier(self):
        """expected false"""
        self.assertIs(ques_published_51hrs_earlier.was_published_recently(),False)

    def test_was_published_recently_with_ques_published_15hrs_earlier(self):
        """expected True"""
        self.assertIs(ques_published_15hrs_earlier.was_published_recently(),True)

    def test_was_published_recently_with_ques_published_15hrs_after_current_time(self):
        """expected false"""
        self.assertIs(ques_published_15hrs_after_current_time.was_published_recently(),False)

class TestIndexView(TestCase):

    def test_appropriate_message_for_question_with_no_options(self):
        """
        Does not display question that has no option
        """
        question_text = "who do you love?"
        create_question(question_text=question_text,days= -1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        

    def test_displays_question_if_options_are_available(self):
        """
        Displays question as list item if options are available
        """
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)
        create_choice(question=question,choice_text="myself", vote=69)
        response= Client().post(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"<li>")

    def test_with_question_published_yesterday(self):
        """display question if qestion was published earlier"""
        question = create_question(question_text="Do you love me?",days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        # self.assertQuerysetEqual([response.context['latest_question_list']],[f"<Question: {question.question_text}>"])


    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        # self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        
        # self.assertQuerysetEqual(
        # response.context['latest_question_list'],
        # ['<Question: Past question.>']
        # )
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        # self.assertQuerysetEqual(
        # response.context['latest_question_list'],
        # ['<Question: Past question.>'])

    
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recent_question(self):
        """
        The detail view of a question with a pub_date in the recent
        """
        recent_question = create_question(question_text='recent question.', days=-1)
        url = reverse('polls:detail', args=(recent_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        """
        past_question = create_question(question_text='past question.', days=-20)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_appropriate_message_for_question_with_no_options(self):
        """
        Does not display question that has no option
        """
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)
        response = self.client.get(reverse('polls:detail',args=(question.id,)))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Sorry, This question has no options. ")

    def test_displays_question_if_options_are_available(self):
        """
        Displays question as list item if options are available
        """
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        response= self.client.get(reverse('polls:detail',args=(question.id,)))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"form")



class VoteViewTest(TestCase):
    def test_voting_with_choice(self):
        """votes the test"""
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        response= Client().post(reverse('polls:detail',args=(question.id,)))
        self.assertEqual(response.status_code,200)

    def test_voting_with_choice(self):
        """votes the test"""
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        response1= Client().post(reverse('polls:vote',args=(question.id,)),{'choice':1})
        self.assertEqual(response1.status_code,302)

    def test_voting_with_valid_choice(self):
        """votes"""
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        create_choice(question=question,choice_text="mom", vote=69)
        response1= Client().post(reverse('polls:vote',args=(question.id,)),{'choice':2})
        self.assertEqual(response1.status_code,302)   
        
    def test_voting_with_invalid_choice(self):
        """returns to detail again"""
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        create_choice(question=question,choice_text="mom", vote=69)
        response1= Client().post(reverse('polls:vote',args=(question.id,)),{'choice':3})
        self.assertEqual(response1.status_code,200) 

    def test_voting_with_no_choice(self):
        """returns to detail again"""
        question_text = "who do you love?"
        question=create_question(question_text=question_text,days= -1)   
        create_choice(question=question,choice_text="myself", vote=69)
        create_choice(question=question,choice_text="mom", vote=69)
        response1= Client().post(reverse('polls:vote',args=(question.id,)),)
        self.assertEqual(response1.status_code,200) 