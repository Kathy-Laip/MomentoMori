--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

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

--
-- Name: memento_mori; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE memento_mori WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';


ALTER DATABASE memento_mori OWNER TO postgres;

\connect memento_mori

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
-- Name: products_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products_categories (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.products_categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.products_categories.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    "client_ID" integer,
    "manager_ID" integer,
    deadmans_name character varying,
    price integer
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: orders_to_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_to_products (
    "order_ID" integer NOT NULL,
    "product_ID" integer NOT NULL,
    amount integer
);


ALTER TABLE public.orders_to_products OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    type character varying NOT NULL,
    category integer NOT NULL,
    amount integer,
    cost_for_one integer,
    details character varying
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    status character varying,
    login character varying,
    password character varying,
    name character varying,
    email character varying,
    phone character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."users_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."users_ID_seq" OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
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
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: products_categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, "client_ID", "manager_ID", deadmans_name, price) FROM stdin;
1	1	2	Латыпов Рустам Хафизович	10000
2	2	3	Долгов Дмитрий Александрович	20000
3	3	1	Михайлов Валерий Юрьевич	10500
\.


--
-- Data for Name: orders_to_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_to_products ("order_ID", "product_ID", amount) FROM stdin;
1	1	1
2	1	1
2	4	1
3	1	1
3	5	1
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, type, category, amount, cost_for_one, details) FROM stdin;
1	товар	1	10	2000	черный
2	товар	1	1	20000	с бархатом
3	товар	2	50	300	розы
6	услуга	5	1	1000	\N
7	услуга	6	1	1500	\N
8	услуга	7	1	1000	\N
9	услуга	8	1	100	\N
10	услуга	9	1	2500	\N
5	товар	4	1	100000	золотой
4	товар	3	10	500	деревянная
\.


--
-- Data for Name: products_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products_categories (id, name) FROM stdin;
1	Гроб
2	Венок
3	Табличка
4	Крест
5	Гробовщик
6	Бальзамировщик
7	Водитель
8	Священник
9	Психолог
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, status, login, password, name, email, phone) FROM stdin;
6	клиент	AAA	dekanatlohi	Андрианова Анастасия Александровна	Anastasiya.Andrianova@kpfu.ru	89364281042
2	менеджер	thyheart	YANABUDGETE	Шляпникова Екатерина Сергеевна	ESShlyapnikova@kpfu.ru	89602356188
5	клиент	34turhiolgw;u4895tlo	wk3rgiy9;pok4ljkn	Еникеев Разиль Радикович	renikeev@kpfu.ru	89462718496
3	менеджер	weredoomed	smertdolgovu	Хамитова Айша Рашидовна	ARKhamitova@kpfu.ru	89172047282
1	менеджер	deathisanillusion	hearthstone	Носова Ксения Евгеньевна	KENosova@kpfu.ru	89204287314
4	клиент	latypov	lapochka	Латыпов Рустам Хафизович	roustam.latypov@kpfu.ru	89242939302
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 9, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 3, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 10, true);


--
-- Name: users_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."users_ID_seq"', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: products_categories categories_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_categories
    ADD CONSTRAINT categories_pk PRIMARY KEY (id);


--
-- Name: orders orders_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pk PRIMARY KEY (id);


--
-- Name: orders_to_products orders_to_products_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_to_products
    ADD CONSTRAINT orders_to_products_pk PRIMARY KEY ("order_ID", "product_ID");


--
-- Name: products products_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pk PRIMARY KEY (id);


--
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- Name: orders_to_products orders_to_products_orders_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_to_products
    ADD CONSTRAINT orders_to_products_orders_id_fk FOREIGN KEY ("order_ID") REFERENCES public.orders(id);


--
-- Name: orders_to_products orders_to_products_products_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_to_products
    ADD CONSTRAINT orders_to_products_products_id_fk FOREIGN KEY ("product_ID") REFERENCES public.products(id);


--
-- Name: orders orders_users_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_users_id_fk FOREIGN KEY ("client_ID") REFERENCES public.users(id);


--
-- Name: orders orders_users_id_fk_2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_users_id_fk_2 FOREIGN KEY ("manager_ID") REFERENCES public.users(id);


--
-- Name: products products_products_categories_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_products_categories_id_fk FOREIGN KEY (category) REFERENCES public.products_categories(id);


--
-- PostgreSQL database dump complete
--

