--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 15.2 (Ubuntu 15.2-1.pgdg20.04+1)

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
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name) FROM stdin;
1	📱 Смартфоны
2	✍️ Планшеты
3	💻 Ноутбуки
6	⌚️ Смарт-часы
5	🖱 Аксессуары
4	🎧 Наушники
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.items (id, name, category_id, price, total, storage, color, description, color_index, item_index, created_at, updated_at) FROM stdin;
7	iPhone 13	1	74000	5	256	Тёмная ночь	\N	1	1	2023-06-08 00:06:47.548944+00	\N
21	iPhone 14	1	83500	5	256	Фиолетовый	\N	4	2	2023-06-08 00:06:47.548944+00	\N
26	iPhone 14	1	93000	5	512	Фиолетовый	\N	4	2	2023-06-08 00:06:47.548944+00	\N
6	iPhone 13	1	65500	5	128	Зелёный	\N	6	1	2023-06-08 00:06:47.548944+00	\N
18	iPhone 14	1	83500	5	256	Голубой	\N	1	2	2023-06-08 00:06:47.548944+00	\N
22	iPhone 14	1	83500	5	256	Красный	\N	5	2	2023-06-08 00:06:47.548944+00	\N
19	iPhone 14	1	83500	5	256	Тёмная ночь (чёрный)	\N	2	2	2023-06-08 00:06:47.548944+00	\N
35	Apple MacBook Pro 13 2022 M2	3	113000	5	256	Space Gray	8 CPU/10 GPU/8 Гб	2	5	2023-06-08 00:06:47.548944+00	\N
36	Apple MacBook Pro 13 2022 M2	3	113000	5	256	Silver	8 CPU/10 GPU/8 Гб	3	5	2023-06-08 00:06:47.548944+00	\N
33	Apple MacBook Air 13 2022 M2	3	105000	5	256	Silver	Apple M2/13.6/2560x1664/8GB/Apple graphics 8-core/Wi-Fi/macOS	3	4	2023-06-08 00:06:47.548944+00	\N
34	Apple MacBook Air 13 2022 M2	3	105000	5	256	Starlight	Apple M2/13.6/2560x1664/8GB/Apple graphics 8-core/Wi-Fi/macOS	1	4	2023-06-08 00:06:47.548944+00	\N
37	Apple iPad 2021 Wi-Fi	2	29000	5	64	Space Gray	\N	1	6	2023-06-08 00:06:47.548944+00	\N
13	iPhone 14	1	70500	5	128	Голубой	\N	1	2	2023-06-08 00:06:47.548944+00	\N
41	Apple iPad 2021 Wi-Fi + Cellular	2	38000	5	64	Space Gray	\N	1	7	2023-06-08 00:06:47.548944+00	\N
42	Apple iPad 2021 Wi-Fi + Cellular	2	38000	5	64	Silver	\N	2	7	2023-06-08 00:06:47.548944+00	\N
40	Apple iPad 2021 Wi-Fi	2	42000	5	256	Silver	\N	2	6	2023-06-08 00:06:47.548944+00	\N
45	Apple iPad 2022 Wi-Fi	2	43000	5	64	Space Gray	\N	1	8	2023-06-08 00:06:47.548944+00	\N
43	Apple iPad 2021 Wi-Fi + Cellular	2	55000	5	256	Space Gray	\N	1	7	2023-06-08 00:06:47.548944+00	\N
46	Apple iPad 2022 Wi-Fi	2	43000	5	64	Silver	\N	2	8	2023-06-08 00:06:47.548944+00	\N
49	Apple iPad 2022 Wi-Fi + Cellular	2	50000	5	64	Space Gray	\N	1	9	2023-06-08 00:06:47.548944+00	\N
3	iPhone 13	1	65500	5	128	Синий	\N	3	1	2023-06-08 00:06:47.548944+00	\N
4	iPhone 13	1	65500	5	128	Розовый	\N	4	1	2023-06-08 00:06:47.548944+00	\N
44	Apple iPad 2021 Wi-Fi + Cellular	2	55000	5	256	Silver	\N	2	7	2023-06-08 00:06:47.548944+00	\N
47	Apple iPad 2022 Wi-Fi	2	55000	5	256	Space Gray	\N	1	8	2023-06-08 00:06:47.548944+00	\N
5	iPhone 13	1	65500	5	128	Красный	\N	5	1	2023-06-08 00:06:47.548944+00	\N
1	iPhone 13	1	65500	5	128	Тёмная ночь	\N	1	1	2023-06-08 00:06:47.548944+00	\N
16	iPhone 14	1	70500	5	128	Фиолетовый	\N	4	2	2023-06-08 00:06:47.548944+00	\N
23	iPhone 14	1	93000	5	512	Голубой	\N	1	2	2023-06-08 00:06:47.548944+00	\N
48	Apple iPad 2022 Wi-Fi	2	55000	5	256	Silver	\N	2	8	2023-06-08 00:06:47.548944+00	\N
51	Apple iPad 2022 Wi-Fi + Cellular	2	65500	5	256	Space Gray	\N	1	9	2023-06-08 00:06:47.548944+00	\N
2	iPhone 13	1	65500	5	128	Сияющая звезда	\N	2	1	2023-06-08 00:06:47.548944+00	\N
28	Apple MacBook Air 13 Late 2020	3	80000	5	256	Space Gray	Apple M1/8GB/Apple graphics 7-core/Wi-Fi/macOS	1	3	2023-06-08 00:06:47.548944+00	\N
29	Apple MacBook Air 13 Late 2020	3	80000	5	256	Silver	Apple M1/8GB/Apple graphics 7-core/Wi-Fi/macOS	2	3	2023-06-08 00:06:47.548944+00	\N
30	Apple MacBook Air 13 Late 2020	3	80000	5	256	Gold	Apple M1/8GB/Apple graphics 7-core/Wi-Fi/macOS	3	3	2023-06-08 00:06:47.548944+00	\N
15	iPhone 14	1	70500	5	128	Сияющая звезда (белый)	\N	3	2	2023-06-08 00:06:47.548944+00	\N
12	iPhone 13	1	74000	5	256	Зелёный	\N	6	1	2023-06-08 00:06:47.548944+00	\N
8	iPhone 13	1	74000	5	256	Сияющая звезда	\N	2	1	2023-06-08 00:06:47.548944+00	\N
27	iPhone 14	1	93000	5	512	Красный	\N	5	2	2023-06-08 00:06:47.548944+00	\N
31	Apple MacBook Air 13 2022 M2	3	105000	5	256	Midnight	Apple M2/13.6/2560x1664/8GB/Apple graphics 8-core/Wi-Fi/macOS	1	4	2023-06-08 00:06:47.548944+00	\N
39	Apple iPad 2021 Wi-Fi	2	42000	5	256	Space Gray	\N	1	6	2023-06-08 00:06:47.548944+00	\N
17	iPhone 14	1	70500	5	128	Красный	\N	5	2	2023-06-08 00:06:47.548944+00	\N
14	iPhone 14	1	70500	5	128	Тёмная ночь (чёрный)	\N	2	2	2023-06-08 00:06:47.548944+00	\N
9	iPhone 13	1	74000	5	256	Синий	\N	3	1	2023-06-08 00:06:47.548944+00	\N
20	iPhone 14	1	83500	5	256	Сияющая звезда (белый)	\N	3	2	2023-06-08 00:06:47.548944+00	\N
10	iPhone 13	1	74000	5	256	Розовый	\N	4	1	2023-06-08 00:06:47.548944+00	\N
24	iPhone 14	1	93000	5	512	Тёмная ночь (чёрный)	\N	2	2	2023-06-08 00:06:47.548944+00	\N
32	Apple MacBook Air 13 2022 M2	3	105000	5	256	Space Gray	Apple M2/13.6/2560x1664/8GB/Apple graphics 8-core/Wi-Fi/macOS	2	4	2023-06-08 00:06:47.548944+00	\N
50	Apple iPad 2022 Wi-Fi + Cellular	2	50000	5	64	Silver	\N	2	9	2023-06-08 00:06:47.548944+00	\N
38	Apple iPad 2021 Wi-Fi	2	29000	5	64	Silver	\N	2	6	2023-06-08 00:06:47.548944+00	\N
25	iPhone 14	1	93000	5	512	Сияющая звезда (белый)	\N	3	2	2023-06-08 00:06:47.548944+00	\N
11	iPhone 13	1	74000	5	256	Красный	\N	5	1	2023-06-08 00:06:47.548944+00	\N
85	Apple iPad Air 2022 Wi-Fi + Cellular	2	67000	5	64	Pink	\N	5	15	2023-06-08 00:06:47.548944+00	\N
65	Apple iPad mini 2021 Wi-Fi + Cellular	2	67000	5	64	Фиолетовый	\N	3	11	2023-06-08 00:06:47.548944+00	\N
68	Apple iPad mini 2021 Wi-Fi + Cellular	2	80000	5	256	Розовый	\N	4	11	2023-06-08 00:06:47.548944+00	\N
82	Apple iPad Air 2022 Wi-Fi	2	62000	5	256	Pink	\N	5	14	2023-06-08 00:06:47.548944+00	\N
83	Apple iPad Air 2022 Wi-Fi + Cellular	2	67000	5	64	Blue	\N	3	15	2023-06-08 00:06:47.548944+00	\N
84	Apple iPad Air 2022 Wi-Fi + Cellular	2	67000	5	64	Purple	\N	4	15	2023-06-08 00:06:47.548944+00	\N
76	Apple iPad Air 2022 Wi-Fi + Cellular	2	80000	5	256	Starlight	\N	2	15	2023-06-08 00:06:47.548944+00	\N
73	Apple iPad Air 2022 Wi-Fi + Cellular	2	67000	5	64	Space Gray	\N	1	15	2023-06-08 00:06:47.548944+00	\N
59	Apple iPad mini 2021 Wi-Fi + Cellular	2	80000	5	256	Серый космос	\N	1	11	2023-06-08 00:06:47.548944+00	\N
78	Apple iPad Air 2022 Wi-Fi	2	43000	5	64	Purple	\N	4	14	2023-06-08 00:06:47.548944+00	\N
97	Apple AirPods Max	4	53000	5	\N	Зелёный	\N	5	22	2023-06-08 00:06:47.548944+00	\N
94	Apple AirPods Max	4	53000	5	\N	Серебристый	\N	2	22	2023-06-08 00:06:47.548944+00	\N
105	Apple Watch SE 2022 44мм корпус из алюминия спортивный ремешок	6	28500	5	\N	Сияющая звезда	\N	2	27	2023-06-08 00:06:47.548944+00	\N
89	Apple AirPods 2	4	11500	5	\N		\N	\N	18	2023-06-08 00:06:47.548944+00	\N
106	Apple Watch SE 2022 44мм корпус из алюминия спортивный ремешок	6	28500	5	\N	Серебристый	\N	3	27	2023-06-08 00:06:47.548944+00	\N
107	Apple Watch Series 8 41мм корпус из алюминия спортивный ремешок	6	35000	5	\N	Тёмная ночь	\N	1	28	2023-06-08 00:06:47.548944+00	\N
91	Apple AirPods Pro MagSafe	4	18000	5	\N		\N	\N	20	2023-06-08 00:06:47.548944+00	\N
92	Apple AirPods Pro 2	4	21000	5	\N		\N	\N	21	2023-06-08 00:06:47.548944+00	\N
103	Apple Watch SE 2022 40мм корпус из алюминия спортивный ремешок	6	26500	5	\N	Серебристый	\N	3	26	2023-06-08 00:06:47.548944+00	\N
95	Apple AirPods Max	4	53000	5	\N	Розовый	\N	3	22	2023-06-08 00:06:47.548944+00	\N
109	Apple Watch Series 8 41мм корпус из алюминия спортивный ремешок	6	35000	5	\N	Белый	\N	3	28	2023-06-08 00:06:47.548944+00	\N
110	Apple Watch Series 8 41мм корпус из алюминия спортивный ремешок	6	35000	5	\N	Красный	\N	4	28	2023-06-08 00:06:47.548944+00	\N
113	Apple Watch Series 8 45мм корпус из алюминия спортивный ремешок	6	37000	5	\N	Белый	\N	3	29	2023-06-08 00:06:47.548944+00	\N
111	Apple Watch Series 8 45мм корпус из алюминия спортивный ремешок	6	37000	5	\N	Тёмная ночь	\N	1	29	2023-06-08 00:06:47.548944+00	\N
54	Apple iPad mini 2021 Wi-Fi	2	43000	5	64	Сияющая звезда	\N	2	10	2023-06-08 00:06:47.548944+00	\N
58	Apple iPad mini 2021 Wi-Fi + Cellular	2	67000	5	64	Сияющая звезда	\N	2	11	2023-06-08 00:06:47.548944+00	\N
79	Apple iPad Air 2022 Wi-Fi	2	43000	5	64	Pink	\N	5	14	2023-06-08 00:06:47.548944+00	\N
93	Apple AirPods Max	4	53000	5	\N	Серый космос	\N	1	22	2023-06-08 00:06:47.548944+00	\N
55	Apple iPad mini 2021 Wi-Fi	2	62000	5	256	Серый космос	\N	1	10	2023-06-08 00:06:47.548944+00	\N
112	Apple Watch Series 8 45мм корпус из алюминия спортивный ремешок	6	37000	5	\N	Сияющая звезда	\N	2	29	2023-06-08 00:06:47.548944+00	\N
53	Apple iPad mini 2021 Wi-Fi	2	43000	5	64	Серый космос	\N	1	10	2023-06-08 00:06:47.548944+00	\N
77	Apple iPad Air 2022 Wi-Fi	2	43000	5	64	Blue	\N	3	14	2023-06-08 00:06:47.548944+00	\N
75	Apple iPad Air 2022 Wi-Fi + Cellular	2	80000	5	256	Space Gray	\N	1	15	2023-06-08 00:06:47.548944+00	\N
71	Apple iPad Air 2022 Wi-Fi	2	62000	5	256	Space Gray	\N	1	14	2023-06-08 00:06:47.548944+00	\N
99	Силиконовый чехол для AirPods Pro	5	500	5	\N	\N	\N	\N	24	2023-06-08 00:06:47.548944+00	\N
69	Apple iPad Air 2022 Wi-Fi	2	43000	5	64	Space Gray	\N	1	14	2023-06-08 00:06:47.548944+00	\N
70	Apple iPad Air 2022 Wi-Fi	2	43000	5	64	Starlight	\N	2	14	2023-06-08 00:06:47.548944+00	\N
62	Apple iPad mini 2021 Wi-Fi	2	43000	5	64	Розовый	\N	4	10	2023-06-08 00:06:47.548944+00	\N
72	Apple iPad Air 2022 Wi-Fi	2	62000	5	256	Starlight	\N	2	14	2023-06-08 00:06:47.548944+00	\N
80	Apple iPad Air 2022 Wi-Fi	2	62000	5	256	Blue	\N	3	14	2023-06-08 00:06:47.548944+00	\N
66	Apple iPad mini 2021 Wi-Fi + Cellular	2	67000	5	64	Розовый	\N	4	11	2023-06-08 00:06:47.548944+00	\N
87	Apple iPad Air 2022 Wi-Fi + Cellular	2	80000	5	256	Purple	\N	4	15	2023-06-08 00:06:47.548944+00	\N
56	Apple iPad mini 2021 Wi-Fi	2	62000	5	256	Сияющая звезда	\N	2	10	2023-06-08 00:06:47.548944+00	\N
52	Apple iPad 2022 Wi-Fi + Cellular	2	65500	5	256	Silver	\N	2	9	2023-06-08 00:06:47.548944+00	\N
74	Apple iPad Air 2022 Wi-Fi + Cellular	2	67000	5	64	Starlight	\N	2	15	2023-06-08 00:06:47.548944+00	\N
86	Apple iPad Air 2022 Wi-Fi + Cellular	2	80000	5	256	Blue	\N	3	15	2023-06-08 00:06:47.548944+00	\N
88	Apple iPad Air 2022 Wi-Fi + Cellular	2	80000	5	256	Pink	\N	5	15	2023-06-08 00:06:47.548944+00	\N
61	Apple iPad mini 2021 Wi-Fi	2	43000	5	64	Фиолетовый	\N	3	10	2023-06-08 00:06:47.548944+00	\N
96	Apple AirPods Max	4	53000	5	\N	Голубое небо	\N	4	22	2023-06-08 00:06:47.548944+00	\N
57	Apple iPad mini 2021 Wi-Fi + Cellular	2	67000	5	64	Серый космос	\N	1	11	2023-06-08 00:06:47.548944+00	\N
64	Apple iPad mini 2021 Wi-Fi	2	62000	5	256	Розовый	\N	4	10	2023-06-08 00:06:47.548944+00	\N
90	Apple AirPods 3	4	17500	5	\N		\N	\N	19	2023-06-08 00:06:47.548944+00	\N
60	Apple iPad mini 2021 Wi-Fi + Cellular	2	80000	5	256	Сияющая звезда	\N	2	11	2023-06-08 00:06:47.548944+00	\N
114	Apple Watch Series 8 45мм корпус из алюминия спортивный ремешок	6	37000	5	\N	Красный	\N	4	29	2023-06-08 00:06:47.548944+00	\N
81	Apple iPad Air 2022 Wi-Fi	2	62000	5	256	Purple	\N	4	14	2023-06-08 00:06:47.548944+00	\N
63	Apple iPad mini 2021 Wi-Fi	2	62000	5	256	Фиолетовый	\N	3	10	2023-06-08 00:06:47.548944+00	\N
115	Apple Watch Ultra 49мм ремешок Alpine Loop	6	76000	5	\N	Зелёный ремешок	\N	1	30	2023-06-08 00:06:47.548944+00	\N
116	Apple Watch Ultra 49мм ремешок Alpine Loop	6	76000	5	\N	Бежевый ремешок	\N	2	30	2023-06-08 00:06:47.548944+00	\N
117	Apple Watch Ultra 49мм ремешок Alpine Loop	6	76000	5	\N	Оранжевый ремешок	\N	3	30	2023-06-08 00:06:47.548944+00	\N
118	Apple Watch Ultra 49мм ремешок Trail Loop	6	76000	5	\N	Black/Gray ремешок	\N	1	31	2023-06-08 00:06:47.548944+00	\N
119	Apple Watch Ultra 49мм ремешок Trail Loop	6	76000	5	\N	Blue/Gray ремешок	\N	2	31	2023-06-08 00:06:47.548944+00	\N
120	Apple Watch Ultra 49мм ремешок Trail Loop	6	76000	5	\N	Yellow/Beige ремешок	\N	3	31	2023-06-08 00:06:47.548944+00	\N
98	Силиконовый чехол для AirPods	5	500	5	\N	\N	\N	\N	23	2023-06-08 00:06:47.548944+00	\N
100	Силиконовый чехол и Защитное стекло для iPhone	5	2990	5	\N	\N	\N	\N	25	2023-06-08 00:06:47.548944+00	\N
101	Apple Watch SE 2022 40мм корпус из алюминия спортивный ремешок	6	26500	5	\N	Тёмная ночь	\N	1	26	2023-06-08 00:06:47.548944+00	\N
102	Apple Watch SE 2022 40мм корпус из алюминия спортивный ремешок	6	26500	5	\N	Сияющая звезда	\N	2	26	2023-06-08 00:06:47.548944+00	\N
104	Apple Watch SE 2022 44мм корпус из алюминия спортивный ремешок	6	28500	5	\N	Тёмная ночь	\N	1	27	2023-06-08 00:06:47.548944+00	\N
108	Apple Watch Series 8 41мм корпус из алюминия спортивный ремешок	6	35000	5	\N	Сияющая звезда	\N	2	28	2023-06-08 00:06:47.548944+00	\N
121	Apple Watch Ultra 49мм ремешок Ocean Band	6	76000	5	\N	Midnight ремешок	\N	1	32	2023-06-08 00:06:47.548944+00	\N
122	Apple Watch Ultra 49мм ремешок Ocean Band	6	76000	5	\N	White ремешок	\N	2	32	2023-06-08 00:06:47.548944+00	\N
123	Apple Watch Ultra 49мм ремешок Ocean Band	6	76000	5	\N	Yellow ремешок	\N	3	32	2023-06-08 00:06:47.548944+00	\N
67	Apple iPad mini 2021 Wi-Fi + Cellular	2	80000	5	256	Фиолетовый	\N	3	11	2023-06-08 00:06:47.548944+00	\N
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, true);


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.items_id_seq', 123, true);


--
-- PostgreSQL database dump complete
--

