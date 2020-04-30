--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: exams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exams (
    id integer NOT NULL,
    author_id integer NOT NULL,
    title character varying NOT NULL,
    exam_hash character varying(10),
    description character varying NOT NULL,
    exercises character varying NOT NULL,
    shuffle_exercises boolean NOT NULL,
    exam_duration integer NOT NULL,
    max_retries integer NOT NULL,
    dt_creation timestamp without time zone NOT NULL,
    from_date timestamp without time zone NOT NULL,
    to_date timestamp without time zone NOT NULL,
    is_archived boolean NOT NULL,
    dt_archive timestamp without time zone
);


ALTER TABLE public.exams OWNER TO postgres;

--
-- Name: exams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exams_id_seq OWNER TO postgres;

--
-- Name: exams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exams_id_seq OWNED BY public.exams.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: students_tries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students_tries (
    id integer NOT NULL,
    student_id integer NOT NULL,
    student_username character varying(128) NOT NULL,
    student_fullname character varying(128) NOT NULL,
    student_picture character varying,
    teacher_id integer NOT NULL,
    teacher_username character varying(128) NOT NULL,
    teacher_fullname character varying(128) NOT NULL,
    teacher_picture character varying,
    exam_id integer NOT NULL,
    title character varying NOT NULL,
    exam_hash character varying(10),
    description character varying NOT NULL,
    exercises character varying NOT NULL,
    exam_duration integer NOT NULL,
    dt_try timestamp without time zone NOT NULL,
    dt_expiration timestamp without time zone NOT NULL,
    current_state integer NOT NULL,
    answers character varying,
    total_score integer,
    student_score integer
);


ALTER TABLE public.students_tries OWNER TO postgres;

--
-- Name: students_tries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_tries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_tries_id_seq OWNER TO postgres;

--
-- Name: students_tries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_tries_id_seq OWNED BY public.students_tries.id;


--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id integer NOT NULL,
    student_id integer NOT NULL,
    exam_id integer NOT NULL,
    dt_subscription timestamp without time zone NOT NULL,
    is_archived boolean NOT NULL,
    dt_archive timestamp without time zone
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscriptions_id_seq OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscriptions_id_seq OWNED BY public.subscriptions.id;


--
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    id integer NOT NULL
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(128) NOT NULL,
    fullname character varying(128) NOT NULL,
    user_type character varying(32) NOT NULL,
    dt_creation timestamp without time zone NOT NULL,
    is_archived boolean NOT NULL,
    dt_archive timestamp without time zone,
    picture character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: exams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams ALTER COLUMN id SET DEFAULT nextval('public.exams_id_seq'::regclass);


--
-- Name: students_tries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_tries ALTER COLUMN id SET DEFAULT nextval('public.students_tries_id_seq'::regclass);


--
-- Name: subscriptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions ALTER COLUMN id SET DEFAULT nextval('public.subscriptions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
74a2ff9eb5c9
\.


--
-- Data for Name: exams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exams (id, author_id, title, exam_hash, description, exercises, shuffle_exercises, exam_duration, max_retries, dt_creation, from_date, to_date, is_archived, dt_archive) FROM stdin;
4	3	CSS MCQ Part 2	\N	This is the second part of the CSS MCQ Exam.	[{"title": "Exercise 1", "description": "There is somtimes more than one correct answer.", "shuffle_questions": true, "questions": [{"title": "Question 1", "description": "Having the following HTML and CSS snippets:\\n<div id=\\"address\\" class=\\"coords\\">\\n<ul>\\n  <li>Help</li>\\n  <li>us</li>\\n  <li>God!</li>\\n</ul>\\n</div>\\nul { \\n  list-style: none; \\n  padding:0; \\n  margin: 0;\\n}\\nul li { \\n  /* 2nd rule */\\n}\\nWhat's the rule that could be placed in the 2nd rule to display the three list items in one line: Help us God!, rather than three lines:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "position: inline;", "is_correct": false, "mark": 1}, {"answer": "display: inline;", "is_correct": true, "mark": 1}, {"answer": "position: inline-block;", "is_correct": false, "mark": 1}, {"answer": "display: inline-block;", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 2", "description": "Having the following HTML and CSS snippets:\\n<div id=\\"address\\" class=\\"coords\\">\\n<ul>\\n  <li>Help</li>\\n  <li>us</li>\\n  <li>God!</li>\\n</ul>\\n</div>\\nul { \\n  list-style: none; \\n  padding:0; \\n  margin: 0;\\n}\\nul li { \\n  /* 2nd rule */\\n}\\nQ10: Which rule could be placed in the 2nd rule to define a 5px horizontal margin between list items:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "margin: 5px 0 5px;", "is_correct": false, "mark": 1}, {"answer": "margin: 0; margin-left: 5px; margin-right: 5px;", "is_correct": true, "mark": 1}, {"answer": "margin: 5px 0;", "is_correct": false, "mark": 1}, {"answer": "margin: 0 5px;", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 3", "description": "Which selector could be used to style the <ul> inside the div?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "#address ul", "is_correct": true, "mark": 1}, {"answer": ".address ul", "is_correct": false, "mark": 1}, {"answer": "#coords ul", "is_correct": false, "mark": 1}, {"answer": ".coords ul", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 4", "description": "How to center one div inside the page?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "text-align: center;", "is_correct": true, "mark": 1}, {"answer": "margin: 0 auto;", "is_correct": false, "mark": 1}, {"answer": "align: center;", "is_correct": false, "mark": 1}, {"answer": "margin: auto 0;", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 5", "description": "Which selector should be used to style in red some (more than one) of the paragraphs in one web page?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Tag selector", "is_correct": false, "mark": 1}, {"answer": "Class selector", "is_correct": true, "mark": 1}, {"answer": "d selector", "is_correct": false, "mark": 1}, {"answer": "Pseudoclass selector", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 6", "description": "How to center one div inside the page?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "text-align: center;", "is_correct": false, "mark": 1}, {"answer": "margin: 0 auto;", "is_correct": true, "mark": 1}, {"answer": "align: center;", "is_correct": false, "mark": 1}, {"answer": "margin: auto 0;", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 7", "description": "Select which properties to add to the following rule to draw a triangle in CSS using borders?\\n#triangle { width: 0; height: 0; }", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "border-bottom: 100px solid red;", "is_correct": true, "mark": 1}, {"answer": "border-right: 100px solid transparent;", "is_correct": true, "mark": 1}, {"answer": "border-left: 100px solid transparent;", "is_correct": true, "mark": 1}, {"answer": "We cannot draw triangles in CSS", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 8", "description": "How to display a (400px x 400px) centered image in the center of one div using CSS?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "background-image: url(imgs/bg.png);", "is_correct": true, "mark": 1}, {"answer": "background-repeat: no-repeat;", "is_correct": true, "mark": 1}, {"answer": "background-size: 100% auto;", "is_correct": true, "mark": 1}, {"answer": "background-position: center center;", "is_correct": true, "mark": 1}], "shuffle_answers": true}]}]	f	3600	1	2020-04-26 18:23:37.939234	2020-04-26 00:00:00	2020-07-25 00:00:00	f	\N
2	3	HTML MCS - Part 2	\N	This is the second part of the MCQ Exam.	[{"title": "Exercise 1", "description": "Every question could have multiple correct answers.", "shuffle_questions": false, "questions": [{"title": "Question 1", "description": "Which facts are True about tables:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "<tr> is used to make rows, <th> is used to make heading cells, <td> is used to make table cells", "is_correct": true, "mark": 1}, {"answer": "cells can span multiple rows and columns", "is_correct": true, "mark": 1}, {"answer": "We should create columns first and than add rows inside them", "is_correct": false, "mark": 1}, {"answer": "Tables are, by default, rendered with an external border", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 2", "description": "To create forms to collect user inputs:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Use <from> tag, then set action and method attributes", "is_correct": false, "mark": 1}, {"answer": "Use <input> tag to create buttons, text inputs, checkboxes and radio buttons.", "is_correct": true, "mark": 1}, {"answer": "Provide a way to submit the data via <input type=\\"submit\\"> or its equivalents", "is_correct": true, "mark": 1}, {"answer": "Use placeholder attribute to give hints to the user about the required input", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 3", "description": "Tick all correct facts. Images:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Are created using the <img> tag", "is_correct": true, "mark": 1}, {"answer": "The src attribute is used to specify the image path", "is_correct": true, "mark": 1}, {"answer": "The href attribute is used to specify the image path", "is_correct": false, "mark": 1}, {"answer": "It's encouraged to add an alt attribute, to be displayed when the image fails to display", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 4", "description": "In which cases should we use absolute URLs?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "To access internal data located on the same webserver", "is_correct": false, "mark": 1}, {"answer": "To access external data located in an external server", "is_correct": true, "mark": 1}, {"answer": "To use another protocol such as file, ftp, https, etc.", "is_correct": true, "mark": 1}, {"answer": "When the resources are located in the same folder as the webpage", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 5", "description": "HTML is built around the idea that one document can references others resources and documents with the ability to move from one to one another.", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "We can create a link using <link> tag", "is_correct": false, "mark": 1}, {"answer": "We can create a link using <a> tag", "is_correct": true, "mark": 1}, {"answer": "We must specify the href attributes and some clickable content", "is_correct": true, "mark": 1}, {"answer": "We can add the target attribute to choose where the document should be opened", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 6", "description": "Which of the following tags are semantic tags added in HTML5:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "header, main, footer, nv", "is_correct": true, "mark": 1}, {"answer": "article, section, aside", "is_correct": true, "mark": 1}, {"answer": "div, span", "is_correct": false, "mark": 1}, {"answer": "p, h1, ul, ol", "is_correct": false, "mark": 1}], "shuffle_answers": true}]}]	f	3600	2147483647	2020-04-26 17:43:20.522904	2020-04-26 00:00:00	2020-07-25 00:00:00	f	\N
3	3	CSS MCQ Exam Part 1	\N	This is the first part of the CSS MCQ	[{"title": "Exercise 1", "description": "There can be more than one correct answer.", "shuffle_questions": false, "questions": [{"title": "Question 1", "description": "What's True about CSS?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "CSS = Cascading Styles Sheets", "is_correct": true, "mark": 1}, {"answer": "It is used to describe page structure", "is_correct": false, "mark": 1}, {"answer": "It is used to describe page formatting", "is_correct": true, "mark": 1}, {"answer": "Multiple style sheets could be included in one HTML file", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 2", "description": "Which of the following ar valid colors:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "#ABCDEF", "is_correct": true, "mark": 1}, {"answer": "rgb(200, 210, 220)", "is_correct": true, "mark": 1}, {"answer": "purple", "is_correct": true, "mark": 1}, {"answer": " hsl(30,50%,50%,1)", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 3", "description": "What's the right syntax for the CSS rules:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "property { selector: value; }", "is_correct": false, "mark": 1}, {"answer": "selector { property: value; }", "is_correct": true, "mark": 1}, {"answer": "value { property: selector; }", "is_correct": false, "mark": 1}, {"answer": "selector (property=value)", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 4", "description": "which properties are used for colors:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "color, to change text color", "is_correct": true, "mark": 1}, {"answer": "background-color, to change the background color", "is_correct": true, "mark": 1}, {"answer": "text-color, to change the text color", "is_correct": false, "mark": 1}, {"answer": "back-color, to change the background color", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 5", "description": "What's the default width of the blue painted box, the rect class was applied to the div.\\nrect {\\n  width: 200px; height: 100px;\\n  margin: 5px 10px 15px 20px;\\n  padding: 5px 10px 15px 20px;\\n  border: 5px solid #333;\\n  background-color: blue;\\n}", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "245px", "is_correct": false, "mark": 1}, {"answer": "265px", "is_correct": false, "mark": 1}, {"answer": "230px", "is_correct": true, "mark": 1}, {"answer": "220px", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 6", "description": "Which is the right property for border-radius to make a [200px x 200px] image looks like a circle:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "100px", "is_correct": true, "mark": 1}, {"answer": "50%", "is_correct": true, "mark": 1}, {"answer": "50px", "is_correct": false, "mark": 1}, {"answer": "100px 100px 100px 100px", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 7", "description": "Tell which property should be placed in the 2nd rule to move the div move from its initial position by 20px to the right and 5px to the to?", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "right: 20px; top: 5px;", "is_correct": false, "mark": 1}, {"answer": "left: 20px; bottom: 5px;", "is_correct": true, "mark": 1}, {"answer": "left: 20px; top: 5px;", "is_correct": false, "mark": 1}, {"answer": "right: 20px; bottom: 5px;", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 8", "description": "Tell which properties should we add to the 2nd rule to make the text 10pt, italic:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "font-size: 10pt; font-style: italic;", "is_correct": true, "mark": 1}, {"answer": "text-size: 10pt; text-style: italic;", "is_correct": false, "mark": 1}, {"answer": "size: 10pt; style: italic;", "is_correct": false, "mark": 1}, {"answer": "font: 10pt italic;", "is_correct": false, "mark": 1}], "shuffle_answers": true}]}]	f	3600	1	2020-04-26 18:01:30.305588	2020-04-26 00:00:00	2020-07-25 00:00:00	f	\N
1	3	HTML MCQ Exam	\N	This is a simple MCS Exam.	[{"title": "Exercise 1 of 1", "description": "There may be one or more correct answer for each of the following questions.", "shuffle_questions": false, "questions": [{"title": "Question 1", "description": "HTML files are rendered by:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Browsers", "is_correct": true, "mark": 1}, {"answer": "Windows", "is_correct": false, "mark": 1}, {"answer": "Python", "is_correct": false, "mark": 1}, {"answer": "Google Chrome/Mozilla Firefox/Brave", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 2", "description": "Websites are often hosted in servers, which:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Are simple computers", "is_correct": true, "mark": 1}, {"answer": "Have softwares that answer user requests", "is_correct": true, "mark": 1}, {"answer": "Are available in network 24h/7days", "is_correct": true, "mark": 1}, {"answer": "Contains only HTML files", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 3", "description": "HTML files could be created using:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Any word processor such Word", "is_correct": false, "mark": 1}, {"answer": "Any text editor", "is_correct": true, "mark": 1}, {"answer": "Just Visual Studio Code", "is_correct": false, "mark": 1}, {"answer": "Web browsers", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 4", "description": "Tags and elements terms are often used interchangeably. In reality:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "They mean the same thing", "is_correct": false, "mark": 1}, {"answer": "Tags are composed of an opening and a closing element inside which there's some content", "is_correct": false, "mark": 1}, {"answer": "Elements are composed of opening and closing tags inside which there's some content", "is_correct": true, "mark": 1}, {"answer": "It depends on the context", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 5", "description": "What are the direct childs of the <html> tag:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "<!doctype HTML>", "is_correct": false, "mark": 1}, {"answer": "<head>", "is_correct": true, "mark": 1}, {"answer": "<body>", "is_correct": true, "mark": 1}, {"answer": "<title>", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 6", "description": "How to define heading in HTML? Using:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "header tag", "is_correct": false, "mark": 1}, {"answer": "<h1> for the smallest heading and <h6> for the biggest", "is_correct": false, "mark": 1}, {"answer": "<h1> for the biggest heading and <h6> for the smallest", "is_correct": true, "mark": 1}, {"answer": "<head> tag", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 7", "description": "The <br> tag can be used to mark the start of a new line.", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "<p> is used to delimit the contents of one paragraph", "is_correct": true, "mark": 1}, {"answer": "<p> could be nested", "is_correct": false, "mark": 1}, {"answer": "<br> can be used inside <p>", "is_correct": true, "mark": 1}, {"answer": "<p> can be used inside <br>", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 8", "description": "HTML defines mainly two types of lists which are:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "Bulleted or ordered lists", "is_correct": false, "mark": 1}, {"answer": "Numbered or unordered lists", "is_correct": false, "mark": 1}, {"answer": "Numbered or ordered lists", "is_correct": true, "mark": 1}, {"answer": "Bulleted or unordered lists", "is_correct": true, "mark": 1}], "shuffle_answers": true}, {"title": "Question 9", "description": "<div> is a general purpose container:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "It could contains others <div>s", "is_correct": true, "mark": 1}, {"answer": "It could not contains others <div>s", "is_correct": false, "mark": 1}, {"answer": "<nav>, <article>, <section> and many others tags are semantic elements that could be replaced by <div>", "is_correct": true, "mark": 1}, {"answer": "have a visible margin above and below them", "is_correct": false, "mark": 1}], "shuffle_answers": true}, {"title": "Question 10", "description": "Many inline tags are used to format text in HTML:", "question_type": "QcmQuestion", "multiple_answers": true, "answers": [{"answer": "<strong> is used to make text italic", "is_correct": false, "mark": 1}, {"answer": "<em> is used to make text bold", "is_correct": false, "mark": 1}, {"answer": "<sup> is used to make text exponent", "is_correct": true, "mark": 1}, {"answer": "<b> is used to make text bold", "is_correct": true, "mark": 1}], "shuffle_answers": true}]}]	f	3600	1	2020-04-26 15:58:10.106531	2020-04-26 00:00:00	2020-07-25 00:00:00	f	\N
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (id) FROM stdin;
2
4
5
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscriptions (id, student_id, exam_id, dt_subscription, is_archived, dt_archive) FROM stdin;
31	5	1	2020-04-28 19:04:02.835919	f	\N
32	5	4	2020-04-28 19:04:05.906891	f	\N
36	4	3	2020-04-29 10:32:32.323587	f	\N
37	4	2	2020-04-29 10:52:28.691926	f	\N
38	4	1	2020-04-30 10:34:28.540926	f	\N
\.


--
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teachers (id) FROM stdin;
1
3
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, fullname, user_type, dt_creation, is_archived, dt_archive, picture) FROM stdin;
4	auth0|5e9182d7d89dee0bdd17cb02	manianis1975@gmail.com	student	2020-04-27 09:34:00.443654	f	\N	https://randomuser.me/api/portraits/lego/2.jpg
1	ktajodbWnCgRYZBZJUGNiknBSYcNui32@clients	mohamed anis layouni	teacher	2020-04-26 13:22:09.563926	f	\N	https://randomuser.me/api/portraits/lego/8.jpg
2	V8IAqOYFsq8vzjF5isGSSJjokelaSMrJ@clients	baher baccouche	student	2020-04-26 13:22:11.362692	f	\N	https://randomuser.me/api/portraits/lego/1.jpg
3	google-oauth2|115983741056323779744	Mani Anis	teacher	2020-04-26 15:58:00.277686	f	\N	https://randomuser.me/api/portraits/lego/6.jpg
5	auth0|5e9c88cd67e8740c1ede1765	manianis@yahoo.fr	student	2020-04-28 16:52:13.013222	f	\N	https://randomuser.me/api/portraits/lego/2.jpg
\.


--
-- Name: exams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exams_id_seq', 4, true);


--
-- Name: students_tries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_tries_id_seq', 12, true);


--
-- Name: subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscriptions_id_seq', 38, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: exams exams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (id);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: students_tries students_tries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_tries
    ADD CONSTRAINT students_tries_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: exams exams_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.teachers(id);


--
-- Name: students students_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: subscriptions subscriptions_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- Name: subscriptions subscriptions_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: teachers teachers_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

