import json
import random
from datetime import datetime, date, timedelta

SAMPLE_EXAMS = [
    {'author_id': 3,
     'description': 'This is a simple MCS Exam.',
     'dt_creation': datetime.datetime(2020, 4, 26, 15, 58, 10, 106531),
     'exam_duration': 3600,
     'exam_hash': None,
     'exercises': json.dumps([{
         'description': 'There may be one or more correct answer for each of '
                        'the following questions.',
         'questions': [{'answers': [
             {'answer': 'Browsers', 'is_correct': True, 'mark': 1},
             {'answer': 'Windows', 'is_correct': False, 'mark': 1},
             {'answer': 'Python', 'is_correct': False, 'mark': 1},
             {'answer': 'Google Chrome/Mozilla Firefox/Brave',
              'is_correct': True,
              'mark': 1}],
             'description': 'HTML files are rendered by:',
             'multiple_answers': True,
             'question_type': 'QcmQuestion',
             'shuffle_answers': True,
             'title': 'Question 1'},
             {'answers': [
                 {'answer': 'Are simple computers',
                  'is_correct': True, 'mark': 1},
                 {
                     'answer': 'Have softwares that answer user requests',
                     'is_correct': True,
                     'mark': 1},
                 {
                     'answer': 'Are available in network 24h/7days',
                     'is_correct': True,
                     'mark': 1},
                 {'answer': 'Contains only HTML files',
                  'is_correct': False,
                  'mark': 1}],
                 'description': 'Websites are often hosted in servers, which:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 2'},
             {'answers': [{
                 'answer': 'Any word processor such Word',
                 'is_correct': False,
                 'mark': 1},
                 {'answer': 'Any text editor',
                  'is_correct': True,
                  'mark': 1},
                 {
                     'answer': 'Just Visual Studio Code',
                     'is_correct': False,
                     'mark': 1},
                 {'answer': 'Web browsers',
                  'is_correct': False,
                  'mark': 1}],
                 'description': 'HTML files could be created using:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 3'},
             {'answers': [
                 {'answer': 'They mean the same thing',
                  'is_correct': False,
                  'mark': 1},
                 {
                     'answer': "Tags are composed of an opening and a closing "
                               "element inside which there's some content",
                     'is_correct': False,
                     'mark': 1},
                 {
                     'answer': "Elements are composed of opening and closing "
                               "tags inside which there's some content",
                     'is_correct': True,
                     'mark': 1},
                 {'answer': 'It depends on the context',
                  'is_correct': False,
                  'mark': 1}],
                 'description': 'Tags and elements terms are often used '
                                'interchangeably. In reality:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 4'},
             {'answers': [{'answer': '<!doctype HTML>',
                           'is_correct': False,
                           'mark': 1},
                          {'answer': '<head>',
                           'is_correct': True,
                           'mark': 1},
                          {'answer': '<body>',
                           'is_correct': True,
                           'mark': 1},
                          {'answer': '<title>',
                           'is_correct': False,
                           'mark': 1}],
              'description': 'What are the direct childs of the <html> tag:',
              'multiple_answers': True,
              'question_type': 'QcmQuestion',
              'shuffle_answers': True,
              'title': 'Question 5'},
             {'answers': [{'answer': 'header tag', 'is_correct': False,
                           'mark': 1},
                          {
                              'answer': '<h1> for the smallest heading and '
                                        '<h6> for the biggest',
                              'is_correct': False, 'mark': 1},
                          {
                              'answer': '<h1> for the biggest heading and '
                                        '<h6> for the smallest',
                              'is_correct': True, 'mark': 1},
                          {'answer': '<head> tag',
                           'is_correct': False,
                           'mark': 1}],
              'description': 'How to define heading in HTML? Using:',
              'multiple_answers': True,
              'question_type': 'QcmQuestion',
              'shuffle_answers': True,
              'title': 'Question 6'},
             {'answers': [{
                 'answer': '<p> is used to delimit the contents of one '
                           'paragraph',
                 'is_correct': True,
                 'mark': 1},
                 {'answer': '<p> could be nested', 'is_correct': False,
                  'mark': 1},
                 {'answer': '<br> can be used inside <p>', 'is_correct': True,
                     'mark': 1},
                 {'answer': '<p> can be used inside <br>', 'is_correct': False,
                     'mark': 1}],
                 'description': 'The <br> tag can be used to mark the start '
                                'of a new line.',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 7'},
             {'answers': [
                 {'answer': 'Bulleted or ordered lists',
                  'is_correct': False,
                  'mark': 1},
                 {
                     'answer': 'Numbered or unordered lists',
                     'is_correct': False,
                     'mark': 1},
                 {'answer': 'Numbered or ordered lists',
                  'is_correct': True,
                  'mark': 1},
                 {
                     'answer': 'Bulleted or unordered lists',
                     'is_correct': True,
                     'mark': 1}],
                 'description': 'HTML defines mainly two types of lists '
                                'which are:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 8'},
             {'answers': [{
                 'answer': 'It could contains others <div>s',
                 'is_correct': True,
                 'mark': 1},
                 {
                     'answer': 'It could not contains others <div>s',
                     'is_correct': False,
                     'mark': 1},
                 {
                     'answer': '<nav>, <article>, <section> and many others tags are '
                               'semantic elements that could be replaced by <div>',
                     'is_correct': True,
                     'mark': 1},
                 {
                     'answer': 'have a visible margin above and below them',
                     'is_correct': False,
                     'mark': 1}],
                 'description': '<div> is a general purpose container:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 9'},
             {'answers': [{
                 'answer': '<strong> is used to make text italic',
                 'is_correct': False,
                 'mark': 1},
                 {
                     'answer': '<em> is used to make text bold',
                     'is_correct': False,
                     'mark': 1},
                 {
                     'answer': '<sup> is used to make text exponent',
                     'is_correct': True,
                     'mark': 1},
                 {
                     'answer': '<b> is used to make text bold',
                     'is_correct': True,
                     'mark': 1}],
                 'description': 'Many inline tags are used to format text in HTML:',
                 'multiple_answers': True,
                 'question_type': 'QcmQuestion',
                 'shuffle_answers': True,
                 'title': 'Question 10'}],
         'shuffle_questions': False,
         'title': 'Exercise 1 of 1'}]),
     'from_date': datetime.datetime(2020, 4, 26, 0, 0),
     'id': 1,
     'max_retries': 2147483647,
     'shuffle_exercises': False,
     'title': 'HTML MCQ Exam',
     'to_date': datetime.datetime(2020, 7, 25, 0, 0)},
    {'author_id': 3,
     'description': 'This is the second part of the MCQ Exam.',
     'dt_creation': datetime.datetime(2020, 4, 26, 17, 43, 20, 522904),
     'exam_duration': 3600,
     'exam_hash': None,
     'exercises': json.dumps([
         {'description': 'Every question could have multiple correct answers.',
          'questions': [{'answers': [
              {'answer': '<tr> is used to make rows, <th> is used to make '
                         'heading cells, <td> is used to make table cells',
               'is_correct': True,
               'mark': 1},
              {'answer': 'cells can span multiple rows and columns',
               'is_correct': True,
               'mark': 1},
              {'answer': 'We should create columns first and than add rows '
                         'inside them',
               'is_correct': False,
               'mark': 1},
              {'answer': 'Tables are, by default, rendered with an external '
                         'border',
               'is_correct': False,
               'mark': 1}],
              'description': 'Which facts are True about tables:',
              'multiple_answers': True,
              'question_type': 'QcmQuestion',
              'shuffle_answers': True,
              'title': 'Question 1'},
              {'answers': [{
                  'answer': 'Use <from> tag, then set action and method attributes',
                  'is_correct': False,
                  'mark': 1},
                  {
                      'answer': 'Use <input> tag to create buttons, text inputs, '
                                'checkboxes and radio buttons.',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'Provide a way to submit the data via <input '
                                'type="submit"> or its equivalents',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'Use placeholder attribute to give hints to the user '
                                'about the required input',
                      'is_correct': True,
                      'mark': 1}],
                  'description': 'To create forms to collect user inputs:',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 2'},
              {'answers': [
                  {'answer': 'Are created using the <img> tag',
                   'is_correct': True,
                   'mark': 1},
                  {
                      'answer': 'The src attribute is used to specify the image path',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'The href attribute is used to specify the image path',
                      'is_correct': False,
                      'mark': 1},
                  {
                      'answer': "It's encouraged to add an alt attribute, to be "
                                'displayed when the image fails to display',
                      'is_correct': True,
                      'mark': 1}],
                  'description': 'Tick all correct facts. Images:',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 3'},
              {'answers': [{
                  'answer': 'To access internal data located on the same webserver',
                  'is_correct': False,
                  'mark': 1},
                  {
                      'answer': 'To access external data located in an external server',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'To use another protocol such as file, ftp, https, etc.',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'When the resources are located in the same folder as '
                                'the webpage',
                      'is_correct': False,
                      'mark': 1}],
                  'description': 'In which cases should we use absolute URLs?',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 4'},
              {'answers': [
                  {'answer': 'We can create a link using <link> tag',
                   'is_correct': False,
                   'mark': 1},
                  {'answer': 'We can create a link using <a> tag',
                   'is_correct': True,
                   'mark': 1},
                  {
                      'answer': 'We must specify the href attributes and some clickable '
                                'content',
                      'is_correct': True,
                      'mark': 1},
                  {
                      'answer': 'We can add the target attribute to choose where the '
                                'document should be opened',
                      'is_correct': True,
                      'mark': 1}],
                  'description': 'HTML is built around the idea that one document can references '
                                 'others resources and documents with the ability to move from one '
                                 'to one another.',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 5'},
              {'answers': [{'answer': 'header, main, footer, nv',
                            'is_correct': True,
                            'mark': 1},
                           {'answer': 'article, section, aside',
                            'is_correct': True, 'mark': 1},
                           {'answer': 'div, span',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'p, h1, ul, ol',
                            'is_correct': False, 'mark': 1}],
               'description': 'Which of the following tags are semantic tags added in HTML5:',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 6'}],
          'shuffle_questions': False,
          'title': 'Exercise 1'}]),
     'from_date': datetime.datetime(2020, 4, 26, 0, 0),
     'id': 2,
     'max_retries': 2147483647,
     'shuffle_exercises': False,
     'title': 'HTML MCS - Part 2',
     'to_date': datetime.datetime(2020, 7, 25, 0, 0)},
    {'author_id': 3,
     'description': 'This is the first part of the CSS MCQ',
     'dt_creation': datetime.datetime(2020, 4, 26, 18, 1, 30, 305588),
     'exam_duration': 3600,
     'exam_hash': None,
     'exercises': json.dumps([
         {'description': 'There can be more than one correct answer.',
          'questions': [
              {'answers': [{'answer': 'CSS = Cascading Styles Sheets',
                            'is_correct': True,
                            'mark': 1},
                           {'answer': 'It is used to describe page structure',
                            'is_correct': False,
                            'mark': 1},
                           {'answer': 'It is used to describe page formatting',
                            'is_correct': True,
                            'mark': 1},
                           {
                               'answer': 'Multiple style sheets could be included in one HTML '
                                         'file',
                               'is_correct': True,
                               'mark': 1}],
               'description': "What's True about CSS?",
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 1'},
              {'answers': [
                  {'answer': '#ABCDEF', 'is_correct': True, 'mark': 1},
                  {'answer': 'rgb(200, 210, 220)', 'is_correct': True,
                   'mark': 1},
                  {'answer': 'purple', 'is_correct': True, 'mark': 1},
                  {'answer': ' hsl(30,50%,50%,1)', 'is_correct': True,
                   'mark': 1}],
                  'description': 'Which of the following ar valid colors:',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 2'},
              {'answers': [{'answer': 'property { selector: value; }',
                            'is_correct': False,
                            'mark': 1},
                           {'answer': 'selector { property: value; }',
                            'is_correct': True,
                            'mark': 1},
                           {'answer': 'value { property: selector; }',
                            'is_correct': False,
                            'mark': 1},
                           {'answer': 'selector (property=value)',
                            'is_correct': False,
                            'mark': 1}],
               'description': "What's the right syntax for the CSS rules:",
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 3'},
              {'answers': [{'answer': 'color, to change text color',
                            'is_correct': True,
                            'mark': 1},
                           {
                               'answer': 'background-color, to change the background color',
                               'is_correct': True,
                               'mark': 1},
                           {'answer': 'text-color, to change the text color',
                            'is_correct': False,
                            'mark': 1},
                           {
                               'answer': 'back-color, to change the background color',
                               'is_correct': False,
                               'mark': 1}],
               'description': 'which properties are used for colors:',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 4'},
              {'answers': [{'answer': '245px', 'is_correct': False, 'mark': 1},
                           {'answer': '265px', 'is_correct': False, 'mark': 1},
                           {'answer': '230px', 'is_correct': True, 'mark': 1},
                           {'answer': '220px', 'is_correct': False,
                            'mark': 1}],
               'description': "What's the default width of the blue painted box, the rect class "
                              'was applied to the div.\n'
                              'rect {\n'
                              '  width: 200px; height: 100px;\n'
                              '  margin: 5px 10px 15px 20px;\n'
                              '  padding: 5px 10px 15px 20px;\n'
                              '  border: 5px solid #333;\n'
                              '  background-color: blue;\n'
                              '}',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 5'},
              {'answers': [{'answer': '100px', 'is_correct': True, 'mark': 1},
                           {'answer': '50%', 'is_correct': True, 'mark': 1},
                           {'answer': '50px', 'is_correct': False, 'mark': 1},
                           {'answer': '100px 100px 100px 100px',
                            'is_correct': True,
                            'mark': 1}],
               'description': 'Which is the right property for border-radius to make a [200px x '
                              '200px] image looks like a circle:',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 6'},
              {'answers': [
                  {'answer': 'right: 20px; top: 5px;', 'is_correct': False,
                   'mark': 1},
                  {'answer': 'left: 20px; bottom: 5px;',
                   'is_correct': True,
                   'mark': 1},
                  {'answer': 'left: 20px; top: 5px;', 'is_correct': False,
                   'mark': 1},
                  {'answer': 'right: 20px; bottom: 5px;',
                   'is_correct': False,
                   'mark': 1}],
                  'description': 'Tell which property should be placed in the 2nd rule to move the '
                                 'div move from its initial position by 20px to the right and 5px '
                                 'to the to?',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 7'},
              {'answers': [{'answer': 'font-size: 10pt; font-style: italic;',
                            'is_correct': True,
                            'mark': 1},
                           {'answer': 'text-size: 10pt; text-style: italic;',
                            'is_correct': False,
                            'mark': 1},
                           {'answer': 'size: 10pt; style: italic;',
                            'is_correct': False,
                            'mark': 1},
                           {'answer': 'font: 10pt italic;',
                            'is_correct': False, 'mark': 1}],
               'description': 'Tell which properties should we add to the 2nd rule to make the '
                              'text 10pt, italic:',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 8'}],
          'shuffle_questions': False,
          'title': 'Exercise 1'}]),
     'from_date': datetime.datetime(2020, 4, 26, 0, 0),
     'id': 3,
     'max_retries': 2147483647,
     'shuffle_exercises': False,
     'title': 'CSS MCQ Exam Part 1',
     'to_date': datetime.datetime(2020, 7, 25, 0, 0)},
    {'author_id': 3,
     'description': 'This is the second part of the CSS MCQ Exam.',
     'dt_creation': datetime.datetime(2020, 4, 26, 18, 23, 37, 939234),
     'exam_duration': 3600,
     'exam_hash': None,
     'exercises': json.dumps([
         {'description': 'There is somtimes more than one correct answer.',
          'questions': [{'answers': [
              {'answer': 'position: inline;', 'is_correct': False, 'mark': 1},
              {'answer': 'display: inline;', 'is_correct': True, 'mark': 1},
              {'answer': 'position: inline-block;',
               'is_correct': False,
               'mark': 1},
              {'answer': 'display: inline-block;', 'is_correct': True,
               'mark': 1}],
              'description': 'Having the following HTML and CSS snippets:\n'
                             '<div id="address" class="coords">\n'
                             '<ul>\n'
                             '  <li>Help</li>\n'
                             '  <li>us</li>\n'
                             '  <li>God!</li>\n'
                             '</ul>\n'
                             '</div>\n'
                             'ul { \n'
                             '  list-style: none; \n'
                             '  padding:0; \n'
                             '  margin: 0;\n'
                             '}\n'
                             'ul li { \n'
                             '  /* 2nd rule */\n'
                             '}\n'
                             "What's the rule that could be placed in the 2nd rule to display "
                             'the three list items in one line: Help us God!, rather than '
                             'three lines:',
              'multiple_answers': True,
              'question_type': 'QcmQuestion',
              'shuffle_answers': True,
              'title': 'Question 1'},
              {'answers': [{'answer': 'margin: 5px 0 5px;',
                            'is_correct': False, 'mark': 1},
                           {
                               'answer': 'margin: 0; margin-left: 5px; margin-right: 5px;',
                               'is_correct': True,
                               'mark': 1},
                           {'answer': 'margin: 5px 0;',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'margin: 0 5px;',
                            'is_correct': True, 'mark': 1}],
               'description': 'Having the following HTML and CSS snippets:\n'
                              '<div id="address" class="coords">\n'
                              '<ul>\n'
                              '  <li>Help</li>\n'
                              '  <li>us</li>\n'
                              '  <li>God!</li>\n'
                              '</ul>\n'
                              '</div>\n'
                              'ul { \n'
                              '  list-style: none; \n'
                              '  padding:0; \n'
                              '  margin: 0;\n'
                              '}\n'
                              'ul li { \n'
                              '  /* 2nd rule */\n'
                              '}\n'
                              'Q10: Which rule could be placed in the 2nd rule to define a 5px '
                              'horizontal margin between list items:',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 2'},
              {'answers': [
                  {'answer': '#address ul', 'is_correct': True,
                   'mark': 1},
                  {'answer': '.address ul', 'is_correct': False,
                   'mark': 1},
                  {'answer': '#coords ul', 'is_correct': False,
                   'mark': 1},
                  {'answer': '.coords ul', 'is_correct': True,
                   'mark': 1}],
                  'description': 'Which selector could be used to style the <ul> inside the div?',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 3'},
              {'answers': [{'answer': 'text-align: center;',
                            'is_correct': True, 'mark': 1},
                           {'answer': 'margin: 0 auto;',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'align: center;',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'margin: auto 0;',
                            'is_correct': True, 'mark': 1}],
               'description': 'How to center one div inside the page?',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 4'},
              {'answers': [
                  {'answer': 'Tag selector', 'is_correct': False,
                   'mark': 1},
                  {'answer': 'Class selector', 'is_correct': True,
                   'mark': 1},
                  {'answer': 'd selector', 'is_correct': False,
                   'mark': 1},
                  {'answer': 'Pseudoclass selector',
                   'is_correct': False, 'mark': 1}],
                  'description': 'Which selector should be used to style in red some (more than '
                                 'one) of the paragraphs in one web page?',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 5'},
              {'answers': [{'answer': 'text-align: center;',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'margin: 0 auto;',
                            'is_correct': True, 'mark': 1},
                           {'answer': 'align: center;',
                            'is_correct': False, 'mark': 1},
                           {'answer': 'margin: auto 0;',
                            'is_correct': False, 'mark': 1}],
               'description': 'How to center one div inside the page?',
               'multiple_answers': True,
               'question_type': 'QcmQuestion',
               'shuffle_answers': True,
               'title': 'Question 6'},
              {'answers': [
                  {'answer': 'border-bottom: 100px solid red;',
                   'is_correct': True,
                   'mark': 1},
                  {
                      'answer': 'border-right: 100px solid transparent;',
                      'is_correct': True,
                      'mark': 1},
                  {'answer': 'border-left: 100px solid transparent;',
                   'is_correct': True,
                   'mark': 1},
                  {'answer': 'We cannot draw triangles in CSS',
                   'is_correct': False,
                   'mark': 1}],
                  'description': 'Select which properties to add to the following rule to draw a '
                                 'triangle in CSS using borders?\n'
                                 '#triangle { width: 0; height: 0; }',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 7'},
              {'answers': [
                  {'answer': 'background-image: url(imgs/bg.png);',
                   'is_correct': True,
                   'mark': 1},
                  {'answer': 'background-repeat: no-repeat;',
                   'is_correct': True,
                   'mark': 1},
                  {'answer': 'background-size: 100% auto;',
                   'is_correct': True,
                   'mark': 1},
                  {'answer': 'background-position: center center;',
                   'is_correct': True,
                   'mark': 1}],
                  'description': 'How to display a (400px x 400px) centered image in the center of '
                                 'one div using CSS?',
                  'multiple_answers': True,
                  'question_type': 'QcmQuestion',
                  'shuffle_answers': True,
                  'title': 'Question 8'}],
          'shuffle_questions': True,
          'title': 'Exercise 1'}]),
     'from_date': datetime.datetime(2020, 4, 26, 0, 0),
     'id': 4,
     'max_retries': 2147483647,
     'shuffle_exercises': False,
     'title': 'CSS MCQ Part 2',
     'to_date': datetime.datetime(2020, 7, 25, 0, 0)
     }
]


def generate_random_exam(teacher_id):
    """Generate a random exam for the 'teacher_id'"""
    exam = {
        **random.choice(SAMPLE_EXAMS),
        'author_id': teacher_id,
        'dt_creation': datetime.now(),
        'from_date': datetime.combine(date.today(), datetime.min.time()),
        'to_date': datetime.combine(
            date.today() + timedelta(days=random.randint(1, 6) * 15),
            datetime.min.time()),
        'id': None,
        'max_retries': random.randint(1, 3),
        'exam_duration': random.randint(1, 8) * 900
    }
    return exam
