--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: baseapp_sub_castes; Type: TABLE; Schema: public; Owner: emisf13; Tablespace: 
--

CREATE TABLE baseapp_sub_castes (
    id integer NOT NULL,
    caste_code character varying(4) NOT NULL,
    caste_name character varying(500) NOT NULL,
    community_id integer NOT NULL
);


ALTER TABLE public.baseapp_sub_castes OWNER TO emisf13;

--
-- Data for Name: baseapp_sub_castes; Type: TABLE DATA; Schema: public; Owner: emisf13
--

COPY baseapp_sub_castes (id, caste_code, caste_name, community_id) FROM stdin;
136	130	Yavana	1
1	1	Agamudayar including Thozhu or Thuluva Vellala	1
2	2	Agaram Vellan Chettiar	1
3	3	Alwar, Azhavar and Alavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
4	4	Servai (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	1
5	5	Nulayar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
6	6	Archakarai Vellala	1
7	7	Aryavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
8	8	Ayira Vaisyar	1
9	9	Badagar	1
10	10	Billava	1
11	11	Bondil	1
12	12	Boyas (except Tiruchirappalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal and Dharmapuri and Krishnagiri Districts)	1
13	13	Chakkala (except Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Madurai, Theni, Dindigul and The Nilgiris Districts)	1
14	14	Chavalakarar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
15	15	Chettu or Chetty (including Kottar Chetty, Elur Chetty, Pathira Chetty, Valayal Chetty, Pudukadai Chetty) (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
16	16	Chowdry	1
17	16B	C.S.I. formerly S.I.U.C. (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
18	17	Donga Dasaris (except Kancheepuram Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	1
19	18	Devangar, Sedar	1
20	19	Dombs (except Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts) Dommars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	1
21	20	Enadi	1
22	21	Ezhavathy (in Kanyakumari Districts and Shenkottah Taluk of Tirunelveli District)	1
23	22	Ezhuthachar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
24	23	Ezhuva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
25	24	Gangavar	1
26	25	Gavara, Gavarai & Vadugar (Vaduvar) (other than Kamma, Kapu, Balija & Reddi)	1
27	26	Gounder	1
28	27	Gowda (including Gammala, Kalali and Anuppa Gounder)	1
29	28	Hegde	1
30	29	Idiga	1
31	30	Illathu Pillaimar, Illuvar, Ezhuvar & Illathar	1
32	31	Jhetty	1
33	32	Jogis (except Kancheepuram, Tiruvallur, Madurai, Theni, Dindigul, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	1
34	33	Kabbera	1
35	34	Kaikolar, Sengunthar	1
36	35	Kaladi (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	1
37	36	Kalari Kurup including Kalari Panicker (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
38	37	Kalingi	1
39	38	Kallar, Easanattu Kallar, Gandharvakottai Kallars (except Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	1
40	39	Kallar Kula Thondaman	1
41	40	Kalveli Gounder	1
42	41	Kambar	1
43	42	Kammalar or Viswakarma, Viswakarmala (including Thattar, Porkollar, Kannar, Karumar, Kollar, Thacher, Kal Thacher, Kamsala and Viswabrahmin)	1
44	43	Kani, Kanisu, Kaniyar Panikkar	1
45	44	Kaniyala Vellalar	1
137	131	Yerukula	1
46	45	Kannada Saineegar, Kannadiyar (Through out the State) and Dasapalanjika (Coimbatore, Erode and the Nilgiris Districts)	1
47	46	Kannadiya Naidu	1
48	47	Karpoora Chettiar	1
49	48	Karuneegar (Seer Karuneegar, Sri Karuneegar, Sarattu Karuneegar, Kaikatti Karuneegar, Mathuvazhi Kanakkar, Sozhi Kanakkar & Sunnambu Karuneegar)	1
50	49	Kasukkara Chettiar	1
51	50	Katesar Pattamkatti	1
52	51	Kavuthiyar	1
53	52	Kerala Mudali	1
54	53	Kharvi	1
55	54	Khatri	1
56	55	Kongu Vaishnava	1
57	56	Kongu Vellalars (including Vellala Gounder, NattuGounder, Narambukatti Gounder, Tirumudi Vellalar, Thondu Vellalar, Pala Gounder, Poosari Gounder, Anuppa Vellala Gounder, Padaithalai, Gounder, Chendalai Gounder, Pavalankatti Vellala Gounder, Palla Vellala Gounder, Sanku Vellala Gounder, & Rathinagiri Gounder)	1
58	57	Koppala Velama	1
59	58	Koteyar	1
60	59	Krishnanvaka (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
61	60	Kudikara Vellalar	1
62	61	Kudumbi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
63	62	Kuga Vellalar	1
64	63	Kunchidigar	1
65	63A	Latin Catholics except Latin Catholic Vannar in Kanyakumari District	1
66	64	Lambadi	1
67	65	Lingayat (Jangama)	1
68	66	Mahratta (NonBrahmin) (including Namadev Mahratta)	1
69	67	Malayar	1
70	68	Male	1
71	69	Maniagar	1
72	70	Maravars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts) (including Karumaravars. Appanad Kondayamkottai Maravar (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts) and Sambanad Maravars (except Sivaganga, Virudhunagar and Ramanathapuram Districts)	1
73	71	Moondrumandai Enbathunalu (84) Ur. Sozhia Vellalar	1
74	72	Mooppan	1
75	73	Muthuraja, Muthuracha, Muttiriyar, Mutharaiyar	1
76	74	Nadar, Shanar & Gramani including Christian Nadar, Christian Shanar and Christian Gramani	1
77	75	Nagaram	1
78	76	Naikkar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
79	77	Nangudi Vellalar	1
80	78	Nanjil Mudali (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
81	79	Odar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
82	80	Odiya	1
83	81	Oottruvalanattu Vellalar	1
84	82	O.P.S. Vellalar	1
85	83	Ovachar	1
86	84	Paiyur Kotta Vellalar	1
87	85	Pamulu	1
88	86	Panar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	1
89	86A	Pandiya Vellalar	1
90	87	Omitted	1
91	88	Kathikarar in Kanyakumari District	1
92	89	Pannirandam Chettiar or Uthama Chettiar	1
93	90	Parkavakulam (including Surithimar Nathamar, Malayamar, Moopanar & Nainar)	1
94	91	Perike (including Perike Balija)	1
95	92	Perumkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
96	93	Podikara Vellalar	1
97	94	Pooluva Gounder	1
98	95	Poraya	1
99	96	Pulavar (in Coimbatore and Erode Districts)	1
100	97	Pulluvar or Pooluvar	1
101	98	Pusala	1
102	99	Reddy (Ganjam)	1
103	100	Sadhu Chetty (including Telugu Chetty Twenty four manai Telugu Chetty)	1
104	101	Sakkaravar or Kavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
105	102	Salivagana	1
106	103	Saliyar, Padmasaliyar, Pattusaliyar, Pattariyar and Adhaviyar	1
107	104	Savalakkarar	1
108	105	Senaithalaivar, Senaikudiyar and IIaivaniar	1
109	105A	Serakula Vellalar	1
110	106	Sourashtra (Patnulkarar)	1
111	107	Sozhia Vellalar (including Sozha Vellalar, Vetrilaikarar, Kodikalkarar and Keeraikarar)	1
112	108	Srisayar	1
113	109	Sundaram Chetty	1
114	110	Thogatta Veerakshatriya	1
115	111	Tholkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
116	112	Tholuva Naicker and Vetalakara Naicker	1
117	113	Omitted	1
118	114	Thoriyar	1
119	115	Ukkirakula Kshatriya Naicker	1
120	116	Uppara, Uppillia and Sagara	1
121	117	Urali Gounder (except Tiruchirapalli Karur, Perambalur and Pudukkottai Districts) and Orudaya Gounder or Oorudaya Gounder (in Madurai and Theni, Dindigul, Coimbatore, Erode, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Salem and Namakkal Districts)	1
122	118	Urikkara Nayakkar	1
123	118A	Virakodi Vellala	1
124	119	Vallambar	1
125	119A	Vallanattu Chettiar	1
126	120	Valmiki	1
127	121	Vaniyar, Vania Chettiar (including Gandla, Ganika, Telikula and Chekkalar)	1
128	122	Veduvar and Vedar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District Where the Community is a Scheduled Castes)	1
129	123	Veerasaiva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
130	124	Velar	1
131	125	Vellan Chettiar	1
132	126	Veluthodathu Nair (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
133	127	Vokkaligar (including Vakkaligar, Okkaligar, Kappaliyar, Kappiliya, Okkaliga Gowda, Okkaliya- Gowder, Okkaliya-Gowda, Okkaliya Gowda)	1
134	128	Wynad Chetty (The Nilgiris District)	1
135	129	Yadhava (including Idaiyar, Telugu Speaking Idaiyar known as Vaduga Ayar or Vaduga Idaiyar or Golla and Asthanthra Golla)	1
164	18A	Latin Catholic Christian Vannar	1
150	12	Oddars (except Thanjavur, Nagapattinam, Thiruvarur, Tiruchirappalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	1
307	12	Pedda Boyar (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	1
308	63b	Latin Catholics in Shencottah Taluk of Tirunelveli District	1
309	12	Kaloddars (except Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem & Namakkal Districts)	1
310	12	Nellorepet Oddars (except Vellore and Thiruvannamalai Districts) Sooramari Oddars (except Salem and Namakkal Districts)	1
311	12	Sooramari Oddars (except Salem and Namakkal Districts)	1
313	38	Kottappal Kallars (except Pudukkottai, Tiruchirapalli, Karur and Permbalur Districts)	1
320	132	Orphans and destitues children who have lost their Parents before reaching the age of ten and are destitutes  and who have nobody else to take care of them either by law or custom  and also who are admitted into any of the Schools or orphanages run by the Government or recognised by the Government.	1
321	131A	Converts to Christianity from any Hindu Backward Classes Community or Most Backward Classes Community (except the Converts to Christianity from Meenavar, Parvatharajakulam, Pattanavar, Sembadavar, Mukkuvar or Mukayar and Paravar) or Denotified Communities	1
392	38	Piramalai Kallars (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	1
393	38	Periyasooriyur Kallars (except Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	1
394	16A	Converts to Christianity from Scheduled Castes irrespective of the generation of conversion (except the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	1
138	1	Ansar	2
139	2	Dekkani Muslims	2
140	3	Dudekula	2
141	4	Labbais including Rowthar and Marakayar (whether their spoken language is Tamil or Urdu)	2
142	5	Mapilla	2
143	6	Sheik	2
144	7	Syed	2
145	1	Ambalakarar	3
146	2	Andipandaram	3
147	2A	Arayar (in Kanyakumari District)	3
148	3	Bestha, Siviar	3
149	4	Bhatraju (Other than Kshatriya Raju)	3
151	6	Dasari	3
152	7	Dommara	3
153	8	Eravallar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Tribe)	3
154	9	Isaivellalar	3
155	10	Jambuvanodai	3
156	11	Jangam	3
157	12	Jogi	3
158	13	Kongu Chettiar (in Coimbatore and Erode Districts only)	3
159	14	Koracha	3
160	15	Kulala (including Kuyavar and Kumbarar)	3
161	16	Kunnuvar Mannadi	3
162	17	Kurumba, Kurumba Goundar	3
163	18	Kuruhini Chetty	3
165	19	Maruthuvar, Navithar, Mangala, Velakattalavar, Velakatalanair and Pronopakari	3
166	20	Mond Golla	3
167	21	Moundadan Chetty	3
168	22	Mahendra, Medara	3
169	23	Mutlakampatti	3
170	24	Narikoravar (Kuruvikars)	3
171	25	Nokkar	3
172	25A	Panisaivan / Panisivan	3
173	26	Vanniakula Kshatriya (including Vanniyar, Vanniya, Vannia Gounder, Gounder or Kander, Padayachi, Palli & Agnikula Kshatriya)	3
174	27	Paravar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is Scheduled Caste)	3
175	27A	Paravar converts to Christianity including the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk in Tirunelveli District)	3
176	28	Meenavar (Parvatharajakulam, Pattanavar, Sembadavar) (including converts to Christianity)	3
177	29	Mukkuvar or Mukayar (including converts to Christianity)	3
178	30	Punnan Vettuva Gounder	3
179	31	Pannayar (other than Kathikarar in Kanyakumari District)	3
180	32	Sathatha Srivaishnava (including Sathani, Chattadi and Chattada Srivaishnava)	3
181	33	Sozhia Chetty	3
182	34	Telugupatty Chetty	3
183	35	Thottia Naicker (including Rajakambalam, Gollavar, Sillavar, Thockalavar, Thozhuva Naicker and Erragollar)	3
184	36	Thondaman	3
185	36A	Thoraiyar (Nilgiris)	3
186	36B	Thoraiyar (Plains)	3
187	37	Valaiyar (including Chettinad Valayars)	3
188	38	Vannar (Salaivai Thozhilalar) (including Agasa, Madivala, Ekali, Rajakula, Veluthadar & Rajaka) (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	3
189	39	Vettaikarar	3
190	40	Vettuva Gounder	3
191	41	Yogeeswarar	3
395	5	Boyar, Oddar	3
396	18A	Latin Catholic Christian Vannar (in Kanyakumari District)	3
397	36C	Transgender or Eunuch (Thirunangai or Aravani)	3
192	1	Adiyan	4
193	2	Aranadan	4
194	3	Eravallan (Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	4
195	4	Irular	4
196	5	Kadar	4
197	6	Kammara	4
198	7	Kanikaran, Kanikkar	4
199	8	Kaniyan, Kanyan	4
200	9	Kattunayakan	4
201	10	Kochu Velan	4
202	11	Konda Kapus	4
203	12	Kondareddis	4
204	13	Koraga	4
205	14	Kota	4
206	15	Kudiya, Melakudi	4
207	16	Kurichchan	4
208	17	Kurumbas	4
209	18	Kurumans	4
210	19	Maha Malasar	4
211	20	Malai Arayan	4
212	21	Malai Pandaram	4
213	22	Malai Vedan	4
214	23	Malakkuravan	4
215	24	Malasar	4
216	25	Malayali	4
217	26	Malayakandi	4
218	27	Mannan	4
219	28	Mudugar, Muduvan	4
220	29	Muthuvan	4
221	30	Pallayan	4
222	31	Palliyan	4
223	32	Palliyar	4
224	33	Paniyan	4
225	34	Sholaga	4
226	35	Toda	4
227	36	Uraly	4
228	2	Adi Dravida	5
229	3	Adi Karnataka	5
230	4	Ajila	5
231	6	Ayyanavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
232	7	Baira	5
233	8	Bakuda	5
234	9	Bandi	5
235	10	Bellara	5
236	11	Bharatar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
237	13	Chalavadi	5
238	14	Chamar, Muchi	5
239	15	Chandala	5
240	16	Cheruman	5
241	17	Devendrakulathan	5
242	18	Dom, Dombara, Paidi, Pano	5
243	19	Domban	5
244	20	Godagali	5
245	21	Godda	5
246	22	Gosangi	5
247	23	Holeya	5
248	24	Jaggali	5
249	25	Jambuvulu	5
250	26	Kadaiyan	5
251	27	Kakkalan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
252	28	Kalladi	5
253	29	Kanakkan, Padanna (in the Nilgiris District)	5
254	30	Karimpalan	5
255	31	Kavara (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
256	32	Koliyan	5
257	33	Koosa	5
258	34	Kootan, Koodan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
259	35	Kudumban	5
260	36	Kuravan, Sidhanar	5
261	39	Maila	5
262	40	Mala	5
263	41	Mannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
264	42	Mavilan	5
265	43	Moger	5
266	44	Mundala	5
267	45	Nalakeyava	5
268	46	Nayadi	5
269	47	Padannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
270	49	Pallan	5
271	50	Palluvan	5
272	51	Pambada	5
273	52	Panan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
274	53	Panchama	5
275	54	Pannadi	5
276	55	Panniandi	5
277	56	Paraiyan, Parayan, Sambavar	5
278	57	Paravan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
279	58	Pathiyan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
280	59	Pulayan, Cheramar	5
281	60	Puthirai Vannan	5
282	61	Raneyar	5
283	62	Samagara	5
284	63	Samban	5
285	64	Sapari	5
286	65	Semman	5
287	66	Thandan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
288	68	Tiruvalluvar	5
289	69	Vallon	5
290	70	Valluvan	5
291	71	Vannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
292	72	Vathiriyan	5
293	73	Velan	5
294	74	Vetan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District).	5
295	75	Vettiyan	5
296	76	Vettuvan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	5
297	1	Adi Andhra	6
298	5	Arunthathiyar	6
299	12	Chakkiliyan	6
300	37	Madari	6
301	38	Madiga	6
302	48	Pagadai	6
303	67	Thoti	6
323	42	Attur Kilnad Koravars (Salem, Namakkal, Cuddalore, Villupuram, Ramanathapuram, Sivaganga and Virudhunagar Districts)	9
324	43	Attur Melnad Koravars (Salem and Namakkal District)	9
325	44	Appanad Kondayam Kottai Maravar (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts)	9
326	45	Ambalakarar (Thanjavur, Nagapattinam, Tiruvarur, Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	9
327	46	Ambalakkarar (Suriyanur, Tiruchirapalli District)	9
328	47	Boyas (Tiruchirapalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal, Dharmapuri and Krishnagiri Districts)	9
329	48	Battu Turkas	9
330	49	C.K. Koravars (Cuddalore and Villupuram Districts)	9
331	50	Chakkala (Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Madurai, Theni, Dindigul and the Nilgiris Districts)	9
332	51	Changyampudi Koravars (Vellore and Thiruvannamalai Districts)	9
333	52	Chettinad Valayars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	9
334	53	Dombs (Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	9
335	54	Dobba Koravars (Salem and Namakkal Districts)	9
336	55	Dommars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	9
337	56	Donga Boya	9
338	57	Donga Ur. Korachas	9
339	58	Devagudi Talayaris	9
340	59	Dobbai Korachas (Tiruchirapalli, Karur Perambalur and Pudukkottai Districts)	9
341	60	Dabi Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Vellore and Thiruvannamalai Districts)	9
342	61	Donga Dasaris (Kancheepuram, Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	9
343	62	Gorrela Dodda Boya	9
344	63	Gudu Dasaris	9
345	64	Gandarvakottai Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Cuddalore and Villupuram Districts)	9
346	65	Gandarvakottai Kallars (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	9
347	66	Inji Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
348	67	Jogis (Kancheepuram, Tiruvallur, Chennai, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	9
349	68	Jambavanodai	9
350	69	Kaladis (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	9
351	70	Kal Oddars (Kancheepuram, Thiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam, Tiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem and Namakkal Districts)	9
352	71	Koravars (Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Pudukkottai, Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Chennai, Madurai, Theni, Dindigul and The Nilgiris Distrists	9
353	72	Kalinji Dabikoravars (Thanjavur, Nagapattinam, Tiruvarur and Pudukkottai Districts)	9
354	73	Kootappal Kallars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
355	74	Kala Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
356	75	Kalavathila Boyas	9
357	76	Kepmaris (Kancheepuram, Tiruvallur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	9
358	77	Maravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts)	9
359	78	Monda Koravars	9
360	79	Monda Golla (Salem and Namakkal Districts)	9
361	80	Mutlakampatti (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
362	81	Nokkars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
363	82	Nellorepet Oddars (Vellore and Thiruvannamalai Districts)	9
364	83	Oddars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	9
365	84	Pedda Boyas (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
366	85	Ponnai Koravars (Vellore and Thiruvannamalai Districts)	9
533	130	Yavana	10
367	86	Piramalai Kallars (Sivagangai, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	9
389	108	Varaganeri Koravars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
368	87	Periya Suriyur Kallars (Tiruchirapalli, Karur, Perambalur, and Pudukkottai Districts)	9
369	88	Padayachi (Vellayan Kuppam in Cuddalore District and Tennore in Tiruchirapalli District)	9
374	93	Sakkaraithamadai Koravars (Vellore and Thiruvannamalai districts)	9
370	89	Punnan Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
373	92	Salem Uppu Koravars (Salem and Namakkal Districts)	9
390	109	Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
371	90	Servai (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
376	95	Sooramari Oddars (Salem and Namakkal Districts)	9
372	91	Salem Melnad Koravars (Madurai, Theni, Dindigul, Coimbatore, Erode, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Salem, Namakkal, Vellore and Thiruvannamalai Districts)	9
375	94	Saranga Palli Koravars	9
377	96	Sembanad Maravars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	9
378	97	Thalli Koravars (Salem and Namakkal Districts)	9
379	98	Telungapatti Chettis (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
382	101	Uppukoravars or Settipalli Koravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Madurai, Theni, Dindigul, Vellore and Thiruvannamalai Districts)	9
380	99	Thottia Naickers (Sivaganga, Virudhunagar, Ramanathapuram, Kancheepuram, Tiruvallur, Thanjavur, Nagapattinam, Karur, Tiruchirapalli, Karur, Perambalur. Pudukkottai, Tirunelveli, Thoothukudi, Salem, Namakkal, Vellore, Thiruvannamalai, Coimbatore & Erode Districts)	9
381	100	Thogamalai Koravars or Kepmaris (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
383	102	Urali Gounders (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
384	103	Wayalpad or Nawalpeta Korachas	9
387	106	Vettaikarar (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	9
385	104	Vaduvarpatti Koravars (Madurai, Theni, Dindigul, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli, Thoothukudi, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	9
386	105	Valayars (Madurai, Theni, Dindigul, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Erode and Coimbatore Districts)	9
388	107	Vetta koravars (Salem and Namakkal District)	9
391	391	General	8
398	1	Agamudayar including Thozhu or Thuluva Vellala	10
399	2	Agaram Vellan Chettiar	10
400	3	Alwar, Azhavar and Alavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
401	4	Servai (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	10
402	5	Nulayar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
403	6	Archakarai Vellala	10
404	7	Aryavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
405	8	Ayira Vaisyar	10
406	9	Badagar	10
407	10	Billava	10
408	11	Bondil	10
409	12	Boyas (except Tiruchirappalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal and Dharmapuri and Krishnagiri Districts)	10
410	13	Chakkala (except Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Madurai, Theni, Dindigul and The Nilgiris Districts)	10
411	14	Chavalakarar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
497	97	Pulluvar or Pooluvar	10
412	15	Chettu or Chetty (including Kottar Chetty, Elur Chetty, Pathira Chetty, Valayal Chetty, Pudukadai Chetty) (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
413	16	Chowdry	10
414	16B	C.S.I. formerly S.I.U.C. (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
415	17	Donga Dasaris (except Kancheepuram Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	10
416	18	Devangar, Sedar	10
417	19	Dombs (except Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts) Dommars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	10
418	20	Enadi	10
419	21	Ezhavathy (in Kanyakumari Districts and Shenkottah Taluk of Tirunelveli District)	10
420	22	Ezhuthachar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
421	23	Ezhuva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
422	24	Gangavar	10
423	25	Gavara, Gavarai & Vadugar (Vaduvar) (other than Kamma, Kapu, Balija & Reddi)	10
424	26	Gounder	10
425	27	Gowda (including Gammala, Kalali and Anuppa Gounder)	10
426	28	Hegde	10
427	29	Idiga	10
428	30	Illathu Pillaimar, Illuvar, Ezhuvar & Illathar	10
429	31	Jhetty	10
430	32	Jogis (except Kancheepuram, Tiruvallur, Madurai, Theni, Dindigul, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	10
431	33	Kabbera	10
432	34	Kaikolar, Sengunthar	10
433	35	Kaladi (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	10
434	36	Kalari Kurup including Kalari Panicker (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
435	37	Kalingi	10
436	38	Kallar, Easanattu Kallar, Gandharvakottai Kallars (except Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	10
437	39	Kallar Kula Thondaman	10
438	40	Kalveli Gounder	10
439	41	Kambar	10
440	42	Kammalar or Viswakarma, Viswakarmala (including Thattar, Porkollar, Kannar, Karumar, Kollar, Thacher, Kal Thacher, Kamsala and Viswabrahmin)	10
441	43	Kani, Kanisu, Kaniyar Panikkar	10
442	44	Kaniyala Vellalar	10
534	131	Yerukula	10
443	45	Kannada Saineegar, Kannadiyar (Through out the State) and Dasapalanjika (Coimbatore, Erode and the Nilgiris Districts)	10
444	46	Kannadiya Naidu	10
445	47	Karpoora Chettiar	10
446	48	Karuneegar (Seer Karuneegar, Sri Karuneegar, Sarattu Karuneegar, Kaikatti Karuneegar, Mathuvazhi Kanakkar, Sozhi Kanakkar & Sunnambu Karuneegar)	10
447	49	Kasukkara Chettiar	10
448	50	Katesar Pattamkatti	10
449	51	Kavuthiyar	10
450	52	Kerala Mudali	10
451	53	Kharvi	10
452	54	Khatri	10
453	55	Kongu Vaishnava	10
454	56	Kongu Vellalars (including Vellala Gounder, NattuGounder, Narambukatti Gounder, Tirumudi Vellalar, Thondu Vellalar, Pala Gounder, Poosari Gounder, Anuppa Vellala Gounder, Padaithalai, Gounder, Chendalai Gounder, Pavalankatti Vellala Gounder, Palla Vellala Gounder, Sanku Vellala Gounder, & Rathinagiri Gounder)	10
455	57	Koppala Velama	10
456	58	Koteyar	10
457	59	Krishnanvaka (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
458	60	Kudikara Vellalar	10
459	61	Kudumbi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
460	62	Kuga Vellalar	10
461	63	Kunchidigar	10
462	63A	Latin Catholics except Latin Catholic Vannar in Kanyakumari District	10
463	64	Lambadi	10
464	65	Lingayat (Jangama)	10
465	66	Mahratta (NonBrahmin) (including Namadev Mahratta)	10
466	67	Malayar	10
467	68	Male	10
468	69	Maniagar	10
469	70	Maravars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts) (including Karumaravars. Appanad Kondayamkottai Maravar (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts) and Sambanad Maravars (except Sivaganga, Virudhunagar and Ramanathapuram Districts)	10
470	71	Moondrumandai Enbathunalu (84) Ur. Sozhia Vellalar	10
471	72	Mooppan	10
472	73	Muthuraja, Muthuracha, Muttiriyar, Mutharaiyar	10
473	74	Nadar, Shanar & Gramani including Christian Nadar, Christian Shanar and Christian Gramani	10
474	75	Nagaram	10
475	76	Naikkar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
476	77	Nangudi Vellalar	10
477	78	Nanjil Mudali (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
478	79	Odar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
479	80	Odiya	10
480	81	Oottruvalanattu Vellalar	10
481	82	O.P.S. Vellalar	10
482	83	Ovachar	10
483	84	Paiyur Kotta Vellalar	10
484	85	Pamulu	10
485	86	Panar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	10
486	86A	Pandiya Vellalar	10
487	87	Omitted	10
488	88	Kathikarar in Kanyakumari District	10
489	89	Pannirandam Chettiar or Uthama Chettiar	10
490	90	Parkavakulam (including Surithimar Nathamar, Malayamar, Moopanar & Nainar)	10
491	91	Perike (including Perike Balija)	10
492	92	Perumkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
493	93	Podikara Vellalar	10
494	94	Pooluva Gounder	10
495	95	Poraya	10
496	96	Pulavar (in Coimbatore and Erode Districts)	10
498	98	Pusala	10
499	99	Reddy (Ganjam)	10
500	100	Sadhu Chetty (including Telugu Chetty Twenty four manai Telugu Chetty)	10
501	101	Sakkaravar or Kavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
502	102	Salivagana	10
503	103	Saliyar, Padmasaliyar, Pattusaliyar, Pattariyar and Adhaviyar	10
504	104	Savalakkarar	10
505	105	Senaithalaivar, Senaikudiyar and IIaivaniar	10
506	105A	Serakula Vellalar	10
507	106	Sourashtra (Patnulkarar)	10
508	107	Sozhia Vellalar (including Sozha Vellalar, Vetrilaikarar, Kodikalkarar and Keeraikarar)	10
509	108	Srisayar	10
510	109	Sundaram Chetty	10
511	110	Thogatta Veerakshatriya	10
512	111	Tholkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
513	112	Tholuva Naicker and Vetalakara Naicker	10
514	113	Omitted	10
515	114	Thoriyar	10
516	115	Ukkirakula Kshatriya Naicker	10
517	116	Uppara, Uppillia and Sagara	10
518	117	Urali Gounder (except Tiruchirapalli Karur, Perambalur and Pudukkottai Districts) and Orudaya Gounder or Oorudaya Gounder (in Madurai and Theni, Dindigul, Coimbatore, Erode, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Salem and Namakkal Districts)	10
519	118	Urikkara Nayakkar	10
520	118A	Virakodi Vellala	10
521	119	Vallambar	10
522	119A	Vallanattu Chettiar	10
523	120	Valmiki	10
524	121	Vaniyar, Vania Chettiar (including Gandla, Ganika, Telikula and Chekkalar)	10
525	122	Veduvar and Vedar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District Where the Community is a Scheduled Castes)	10
526	123	Veerasaiva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
527	124	Velar	10
528	125	Vellan Chettiar	10
529	126	Veluthodathu Nair (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
530	127	Vokkaligar (including Vakkaligar, Okkaligar, Kappaliyar, Kappiliya, Okkaliga Gowda, Okkaliya- Gowder, Okkaliya-Gowda, Okkaliya Gowda)	10
531	128	Wynad Chetty (The Nilgiris District)	10
532	129	Yadhava (including Idaiyar, Telugu Speaking Idaiyar known as Vaduga Ayar or Vaduga Idaiyar or Golla and Asthanthra Golla)	10
535	18A	Latin Catholic Christian Vannar	10
536	12	Oddars (except Thanjavur, Nagapattinam, Thiruvarur, Tiruchirappalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	10
537	12	Pedda Boyar (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	10
538	63b	Latin Catholics in Shencottah Taluk of Tirunelveli District	10
539	12	Kaloddars (except Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem & Namakkal Districts)	10
540	12	Nellorepet Oddars (except Vellore and Thiruvannamalai Districts) Sooramari Oddars (except Salem and Namakkal Districts)	10
541	12	Sooramari Oddars (except Salem and Namakkal Districts)	10
542	38	Kottappal Kallars (except Pudukkottai, Tiruchirapalli, Karur and Permbalur Districts)	10
543	132	Orphans and destitues children who have lost their Parents before reaching the age of ten and are destitutes  and who have nobody else to take care of them either by law or custom  and also who are admitted into any of the Schools or orphanages run by the Government or recognised by the Government.	10
544	131A	Converts to Christianity from any Hindu Backward Classes Community or Most Backward Classes Community (except the Converts to Christianity from Meenavar, Parvatharajakulam, Pattanavar, Sembadavar, Mukkuvar or Mukayar and Paravar) or Denotified Communities	10
545	38	Piramalai Kallars (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	10
546	38	Periyasooriyur Kallars (except Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	10
547	16A	Converts to Christianity from Scheduled Castes irrespective of the generation of conversion (except the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	10
548	1	Ambalakarar	11
549	2	Andipandaram	11
550	2A	Arayar (in Kanyakumari District)	11
551	3	Bestha, Siviar	11
552	4	Bhatraju (Other than Kshatriya Raju)	11
553	6	Dasari	11
554	7	Dommara	11
555	8	Eravallar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Tribe)	11
556	9	Isaivellalar	11
557	10	Jambuvanodai	11
558	11	Jangam	11
559	12	Jogi	11
560	13	Kongu Chettiar (in Coimbatore and Erode Districts only)	11
561	14	Koracha	11
562	15	Kulala (including Kuyavar and Kumbarar)	11
563	16	Kunnuvar Mannadi	11
564	17	Kurumba, Kurumba Goundar	11
565	18	Kuruhini Chetty	11
566	19	Maruthuvar, Navithar, Mangala, Velakattalavar, Velakatalanair and Pronopakari	11
567	20	Mond Golla	11
568	21	Moundadan Chetty	11
569	22	Mahendra, Medara	11
570	23	Mutlakampatti	11
571	24	Narikoravar (Kuruvikars)	11
572	25	Nokkar	11
573	25A	Panisaivan / Panisivan	11
574	26	Vanniakula Kshatriya (including Vanniyar, Vanniya, Vannia Gounder, Gounder or Kander, Padayachi, Palli & Agnikula Kshatriya)	11
575	27	Paravar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is Scheduled Caste)	11
576	27A	Paravar converts to Christianity including the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk in Tirunelveli District)	11
577	28	Meenavar (Parvatharajakulam, Pattanavar, Sembadavar) (including converts to Christianity)	11
578	29	Mukkuvar or Mukayar (including converts to Christianity)	11
579	30	Punnan Vettuva Gounder	11
580	31	Pannayar (other than Kathikarar in Kanyakumari District)	11
581	32	Sathatha Srivaishnava (including Sathani, Chattadi and Chattada Srivaishnava)	11
582	33	Sozhia Chetty	11
583	34	Telugupatty Chetty	11
584	35	Thottia Naicker (including Rajakambalam, Gollavar, Sillavar, Thockalavar, Thozhuva Naicker and Erragollar)	11
585	36	Thondaman	11
586	36A	Thoraiyar (Nilgiris)	11
587	36B	Thoraiyar (Plains)	11
588	37	Valaiyar (including Chettinad Valayars)	11
589	38	Vannar (Salaivai Thozhilalar) (including Agasa, Madivala, Ekali, Rajakula, Veluthadar & Rajaka) (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	11
590	39	Vettaikarar	11
591	40	Vettuva Gounder	11
592	41	Yogeeswarar	11
593	5	Boyar, Oddar	11
594	18A	Latin Catholic Christian Vannar (in Kanyakumari District)	11
595	36C	Transgender or Eunuch (Thirunangai or Aravani)	11
596	391	General	12
597	42	Attur Kilnad Koravars (Salem, Namakkal, Cuddalore, Villupuram, Ramanathapuram, Sivaganga and Virudhunagar Districts)	13
598	43	Attur Melnad Koravars (Salem and Namakkal District)	13
599	44	Appanad Kondayam Kottai Maravar (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts)	13
600	45	Ambalakarar (Thanjavur, Nagapattinam, Tiruvarur, Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	13
601	46	Ambalakkarar (Suriyanur, Tiruchirapalli District)	13
602	47	Boyas (Tiruchirapalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal, Dharmapuri and Krishnagiri Districts)	13
603	48	Battu Turkas	13
604	49	C.K. Koravars (Cuddalore and Villupuram Districts)	13
605	50	Chakkala (Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Madurai, Theni, Dindigul and the Nilgiris Districts)	13
606	51	Changyampudi Koravars (Vellore and Thiruvannamalai Districts)	13
607	52	Chettinad Valayars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	13
608	53	Dombs (Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	13
609	54	Dobba Koravars (Salem and Namakkal Districts)	13
679	15	Kudiya, Melakudi	14
610	55	Dommars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	13
611	56	Donga Boya	13
612	57	Donga Ur. Korachas	13
613	58	Devagudi Talayaris	13
614	59	Dobbai Korachas (Tiruchirapalli, Karur Perambalur and Pudukkottai Districts)	13
615	60	Dabi Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Vellore and Thiruvannamalai Districts)	13
616	61	Donga Dasaris (Kancheepuram, Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	13
617	62	Gorrela Dodda Boya	13
618	63	Gudu Dasaris	13
619	64	Gandarvakottai Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Cuddalore and Villupuram Districts)	13
620	65	Gandarvakottai Kallars (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	13
621	66	Inji Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
622	67	Jogis (Kancheepuram, Tiruvallur, Chennai, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	13
623	68	Jambavanodai	13
624	69	Kaladis (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	13
625	70	Kal Oddars (Kancheepuram, Thiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam, Tiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem and Namakkal Districts)	13
626	71	Koravars (Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Pudukkottai, Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Chennai, Madurai, Theni, Dindigul and The Nilgiris Distrists	13
627	72	Kalinji Dabikoravars (Thanjavur, Nagapattinam, Tiruvarur and Pudukkottai Districts)	13
628	73	Kootappal Kallars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
629	74	Kala Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
630	75	Kalavathila Boyas	13
631	76	Kepmaris (Kancheepuram, Tiruvallur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	13
632	77	Maravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts)	13
633	78	Monda Koravars	13
634	79	Monda Golla (Salem and Namakkal Districts)	13
635	80	Mutlakampatti (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
636	81	Nokkars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
637	82	Nellorepet Oddars (Vellore and Thiruvannamalai Districts)	13
638	83	Oddars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	13
639	84	Pedda Boyas (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
640	85	Ponnai Koravars (Vellore and Thiruvannamalai Districts)	13
641	86	Piramalai Kallars (Sivagangai, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	13
642	108	Varaganeri Koravars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
643	87	Periya Suriyur Kallars (Tiruchirapalli, Karur, Perambalur, and Pudukkottai Districts)	13
644	88	Padayachi (Vellayan Kuppam in Cuddalore District and Tennore in Tiruchirapalli District)	13
645	93	Sakkaraithamadai Koravars (Vellore and Thiruvannamalai districts)	13
646	89	Punnan Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
827	120	Valmiki	16
647	92	Salem Uppu Koravars (Salem and Namakkal Districts)	13
648	109	Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
649	90	Servai (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
650	95	Sooramari Oddars (Salem and Namakkal Districts)	13
651	91	Salem Melnad Koravars (Madurai, Theni, Dindigul, Coimbatore, Erode, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Salem, Namakkal, Vellore and Thiruvannamalai Districts)	13
652	94	Saranga Palli Koravars	13
653	96	Sembanad Maravars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	13
654	97	Thalli Koravars (Salem and Namakkal Districts)	13
655	98	Telungapatti Chettis (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
656	101	Uppukoravars or Settipalli Koravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Madurai, Theni, Dindigul, Vellore and Thiruvannamalai Districts)	13
657	99	Thottia Naickers (Sivaganga, Virudhunagar, Ramanathapuram, Kancheepuram, Tiruvallur, Thanjavur, Nagapattinam, Karur, Tiruchirapalli, Karur, Perambalur. Pudukkottai, Tirunelveli, Thoothukudi, Salem, Namakkal, Vellore, Thiruvannamalai, Coimbatore & Erode Districts)	13
658	100	Thogamalai Koravars or Kepmaris (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
659	102	Urali Gounders (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
660	103	Wayalpad or Nawalpeta Korachas	13
661	106	Vettaikarar (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	13
662	104	Vaduvarpatti Koravars (Madurai, Theni, Dindigul, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli, Thoothukudi, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	13
663	105	Valayars (Madurai, Theni, Dindigul, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Erode and Coimbatore Districts)	13
664	107	Vetta koravars (Salem and Namakkal District)	13
665	1	Adiyan	14
666	2	Aranadan	14
667	3	Eravallan (Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	14
668	4	Irular	14
669	5	Kadar	14
670	6	Kammara	14
671	7	Kanikaran, Kanikkar	14
672	8	Kaniyan, Kanyan	14
673	9	Kattunayakan	14
674	10	Kochu Velan	14
675	11	Konda Kapus	14
676	12	Kondareddis	14
677	13	Koraga	14
678	14	Kota	14
680	16	Kurichchan	14
681	17	Kurumbas	14
682	18	Kurumans	14
683	19	Maha Malasar	14
684	20	Malai Arayan	14
685	21	Malai Pandaram	14
686	22	Malai Vedan	14
687	23	Malakkuravan	14
688	24	Malasar	14
689	25	Malayali	14
690	26	Malayakandi	14
691	27	Mannan	14
692	28	Mudugar, Muduvan	14
693	29	Muthuvan	14
694	30	Pallayan	14
695	31	Palliyan	14
696	32	Palliyar	14
697	33	Paniyan	14
698	34	Sholaga	14
699	35	Toda	14
700	36	Uraly	14
701	391	General	15
702	1	Agamudayar including Thozhu or Thuluva Vellala	16
703	2	Agaram Vellan Chettiar	16
704	3	Alwar, Azhavar and Alavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
705	4	Servai (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	16
706	5	Nulayar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
707	6	Archakarai Vellala	16
708	7	Aryavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
709	8	Ayira Vaisyar	16
710	9	Badagar	16
711	10	Billava	16
712	11	Bondil	16
713	12	Boyas (except Tiruchirappalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal and Dharmapuri and Krishnagiri Districts)	16
714	13	Chakkala (except Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Madurai, Theni, Dindigul and The Nilgiris Districts)	16
715	14	Chavalakarar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
716	15	Chettu or Chetty (including Kottar Chetty, Elur Chetty, Pathira Chetty, Valayal Chetty, Pudukadai Chetty) (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
717	16	Chowdry	16
718	16B	C.S.I. formerly S.I.U.C. (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
719	17	Donga Dasaris (except Kancheepuram Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	16
720	18	Devangar, Sedar	16
721	19	Dombs (except Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts) Dommars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	16
722	20	Enadi	16
723	21	Ezhavathy (in Kanyakumari Districts and Shenkottah Taluk of Tirunelveli District)	16
724	22	Ezhuthachar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
725	23	Ezhuva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
726	24	Gangavar	16
727	25	Gavara, Gavarai & Vadugar (Vaduvar) (other than Kamma, Kapu, Balija & Reddi)	16
728	26	Gounder	16
729	27	Gowda (including Gammala, Kalali and Anuppa Gounder)	16
730	28	Hegde	16
731	29	Idiga	16
732	30	Illathu Pillaimar, Illuvar, Ezhuvar & Illathar	16
733	31	Jhetty	16
734	32	Jogis (except Kancheepuram, Tiruvallur, Madurai, Theni, Dindigul, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	16
735	33	Kabbera	16
736	34	Kaikolar, Sengunthar	16
828	121	Vaniyar, Vania Chettiar (including Gandla, Ganika, Telikula and Chekkalar)	16
737	35	Kaladi (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	16
738	36	Kalari Kurup including Kalari Panicker (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
739	37	Kalingi	16
740	38	Kallar, Easanattu Kallar, Gandharvakottai Kallars (except Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	16
741	39	Kallar Kula Thondaman	16
742	40	Kalveli Gounder	16
743	41	Kambar	16
744	42	Kammalar or Viswakarma, Viswakarmala (including Thattar, Porkollar, Kannar, Karumar, Kollar, Thacher, Kal Thacher, Kamsala and Viswabrahmin)	16
745	43	Kani, Kanisu, Kaniyar Panikkar	16
746	44	Kaniyala Vellalar	16
747	45	Kannada Saineegar, Kannadiyar (Through out the State) and Dasapalanjika (Coimbatore, Erode and the Nilgiris Districts)	16
748	46	Kannadiya Naidu	16
749	47	Karpoora Chettiar	16
750	48	Karuneegar (Seer Karuneegar, Sri Karuneegar, Sarattu Karuneegar, Kaikatti Karuneegar, Mathuvazhi Kanakkar, Sozhi Kanakkar & Sunnambu Karuneegar)	16
751	49	Kasukkara Chettiar	16
752	50	Katesar Pattamkatti	16
753	51	Kavuthiyar	16
754	52	Kerala Mudali	16
755	53	Kharvi	16
756	54	Khatri	16
757	55	Kongu Vaishnava	16
758	56	Kongu Vellalars (including Vellala Gounder, NattuGounder, Narambukatti Gounder, Tirumudi Vellalar, Thondu Vellalar, Pala Gounder, Poosari Gounder, Anuppa Vellala Gounder, Padaithalai, Gounder, Chendalai Gounder, Pavalankatti Vellala Gounder, Palla Vellala Gounder, Sanku Vellala Gounder, & Rathinagiri Gounder)	16
759	57	Koppala Velama	16
760	58	Koteyar	16
761	59	Krishnanvaka (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
762	60	Kudikara Vellalar	16
763	61	Kudumbi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
764	62	Kuga Vellalar	16
765	63	Kunchidigar	16
766	63A	Latin Catholics except Latin Catholic Vannar in Kanyakumari District	16
767	64	Lambadi	16
768	65	Lingayat (Jangama)	16
769	66	Mahratta (NonBrahmin) (including Namadev Mahratta)	16
770	67	Malayar	16
771	68	Male	16
772	69	Maniagar	16
773	70	Maravars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts) (including Karumaravars. Appanad Kondayamkottai Maravar (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts) and Sambanad Maravars (except Sivaganga, Virudhunagar and Ramanathapuram Districts)	16
774	71	Moondrumandai Enbathunalu (84) Ur. Sozhia Vellalar	16
775	72	Mooppan	16
776	73	Muthuraja, Muthuracha, Muttiriyar, Mutharaiyar	16
777	74	Nadar, Shanar & Gramani including Christian Nadar, Christian Shanar and Christian Gramani	16
778	75	Nagaram	16
779	76	Naikkar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
780	77	Nangudi Vellalar	16
781	78	Nanjil Mudali (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
782	79	Odar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
783	80	Odiya	16
784	81	Oottruvalanattu Vellalar	16
785	82	O.P.S. Vellalar	16
786	83	Ovachar	16
787	84	Paiyur Kotta Vellalar	16
788	85	Pamulu	16
789	86	Panar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	16
790	86A	Pandiya Vellalar	16
791	87	Omitted	16
792	88	Kathikarar in Kanyakumari District	16
793	89	Pannirandam Chettiar or Uthama Chettiar	16
794	90	Parkavakulam (including Surithimar Nathamar, Malayamar, Moopanar & Nainar)	16
795	91	Perike (including Perike Balija)	16
796	92	Perumkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
797	93	Podikara Vellalar	16
798	94	Pooluva Gounder	16
799	95	Poraya	16
800	96	Pulavar (in Coimbatore and Erode Districts)	16
801	97	Pulluvar or Pooluvar	16
802	98	Pusala	16
803	99	Reddy (Ganjam)	16
804	100	Sadhu Chetty (including Telugu Chetty Twenty four manai Telugu Chetty)	16
805	101	Sakkaravar or Kavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
806	102	Salivagana	16
807	103	Saliyar, Padmasaliyar, Pattusaliyar, Pattariyar and Adhaviyar	16
808	104	Savalakkarar	16
809	105	Senaithalaivar, Senaikudiyar and IIaivaniar	16
810	105A	Serakula Vellalar	16
811	106	Sourashtra (Patnulkarar)	16
812	107	Sozhia Vellalar (including Sozha Vellalar, Vetrilaikarar, Kodikalkarar and Keeraikarar)	16
813	108	Srisayar	16
814	109	Sundaram Chetty	16
815	110	Thogatta Veerakshatriya	16
816	111	Tholkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
817	112	Tholuva Naicker and Vetalakara Naicker	16
818	113	Omitted	16
819	114	Thoriyar	16
820	115	Ukkirakula Kshatriya Naicker	16
821	116	Uppara, Uppillia and Sagara	16
822	117	Urali Gounder (except Tiruchirapalli Karur, Perambalur and Pudukkottai Districts) and Orudaya Gounder or Oorudaya Gounder (in Madurai and Theni, Dindigul, Coimbatore, Erode, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Salem and Namakkal Districts)	16
823	118	Urikkara Nayakkar	16
824	118A	Virakodi Vellala	16
825	119	Vallambar	16
826	119A	Vallanattu Chettiar	16
829	122	Veduvar and Vedar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District Where the Community is a Scheduled Castes)	16
830	123	Veerasaiva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
831	124	Velar	16
832	125	Vellan Chettiar	16
833	126	Veluthodathu Nair (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
834	127	Vokkaligar (including Vakkaligar, Okkaligar, Kappaliyar, Kappiliya, Okkaliga Gowda, Okkaliya- Gowder, Okkaliya-Gowda, Okkaliya Gowda)	16
835	128	Wynad Chetty (The Nilgiris District)	16
836	129	Yadhava (including Idaiyar, Telugu Speaking Idaiyar known as Vaduga Ayar or Vaduga Idaiyar or Golla and Asthanthra Golla)	16
837	130	Yavana	16
838	131	Yerukula	16
839	18A	Latin Catholic Christian Vannar	16
840	12	Oddars (except Thanjavur, Nagapattinam, Thiruvarur, Tiruchirappalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	16
841	12	Pedda Boyar (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	16
842	63b	Latin Catholics in Shencottah Taluk of Tirunelveli District	16
843	12	Kaloddars (except Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem & Namakkal Districts)	16
844	12	Nellorepet Oddars (except Vellore and Thiruvannamalai Districts) Sooramari Oddars (except Salem and Namakkal Districts)	16
845	12	Sooramari Oddars (except Salem and Namakkal Districts)	16
846	38	Kottappal Kallars (except Pudukkottai, Tiruchirapalli, Karur and Permbalur Districts)	16
847	132	Orphans and destitues children who have lost their Parents before reaching the age of ten and are destitutes  and who have nobody else to take care of them either by law or custom  and also who are admitted into any of the Schools or orphanages run by the Government or recognised by the Government.	16
848	131A	Converts to Christianity from any Hindu Backward Classes Community or Most Backward Classes Community (except the Converts to Christianity from Meenavar, Parvatharajakulam, Pattanavar, Sembadavar, Mukkuvar or Mukayar and Paravar) or Denotified Communities	16
849	38	Piramalai Kallars (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	16
964	32	Koliyan	19
965	33	Koosa	19
850	38	Periyasooriyur Kallars (except Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	16
851	16A	Converts to Christianity from Scheduled Castes irrespective of the generation of conversion (except the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	16
852	1	Ambalakarar	17
853	2	Andipandaram	17
854	2A	Arayar (in Kanyakumari District)	17
855	3	Bestha, Siviar	17
856	4	Bhatraju (Other than Kshatriya Raju)	17
857	6	Dasari	17
858	7	Dommara	17
859	8	Eravallar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Tribe)	17
860	9	Isaivellalar	17
861	10	Jambuvanodai	17
862	11	Jangam	17
863	12	Jogi	17
864	13	Kongu Chettiar (in Coimbatore and Erode Districts only)	17
865	14	Koracha	17
866	15	Kulala (including Kuyavar and Kumbarar)	17
867	16	Kunnuvar Mannadi	17
868	17	Kurumba, Kurumba Goundar	17
869	18	Kuruhini Chetty	17
870	19	Maruthuvar, Navithar, Mangala, Velakattalavar, Velakatalanair and Pronopakari	17
871	20	Mond Golla	17
872	21	Moundadan Chetty	17
873	22	Mahendra, Medara	17
874	23	Mutlakampatti	17
875	24	Narikoravar (Kuruvikars)	17
876	25	Nokkar	17
877	25A	Panisaivan / Panisivan	17
878	26	Vanniakula Kshatriya (including Vanniyar, Vanniya, Vannia Gounder, Gounder or Kander, Padayachi, Palli & Agnikula Kshatriya)	17
879	27	Paravar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is Scheduled Caste)	17
880	27A	Paravar converts to Christianity including the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk in Tirunelveli District)	17
881	28	Meenavar (Parvatharajakulam, Pattanavar, Sembadavar) (including converts to Christianity)	17
882	29	Mukkuvar or Mukayar (including converts to Christianity)	17
883	30	Punnan Vettuva Gounder	17
884	31	Pannayar (other than Kathikarar in Kanyakumari District)	17
885	32	Sathatha Srivaishnava (including Sathani, Chattadi and Chattada Srivaishnava)	17
886	33	Sozhia Chetty	17
887	34	Telugupatty Chetty	17
888	35	Thottia Naicker (including Rajakambalam, Gollavar, Sillavar, Thockalavar, Thozhuva Naicker and Erragollar)	17
889	36	Thondaman	17
890	36A	Thoraiyar (Nilgiris)	17
891	36B	Thoraiyar (Plains)	17
892	37	Valaiyar (including Chettinad Valayars)	17
893	38	Vannar (Salaivai Thozhilalar) (including Agasa, Madivala, Ekali, Rajakula, Veluthadar & Rajaka) (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	17
894	39	Vettaikarar	17
895	40	Vettuva Gounder	17
896	41	Yogeeswarar	17
897	5	Boyar, Oddar	17
898	18A	Latin Catholic Christian Vannar (in Kanyakumari District)	17
899	36C	Transgender or Eunuch (Thirunangai or Aravani)	17
900	1	Adiyan	18
901	2	Aranadan	18
902	3	Eravallan (Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	18
903	4	Irular	18
904	5	Kadar	18
905	6	Kammara	18
906	7	Kanikaran, Kanikkar	18
907	8	Kaniyan, Kanyan	18
908	9	Kattunayakan	18
909	10	Kochu Velan	18
910	11	Konda Kapus	18
911	12	Kondareddis	18
912	13	Koraga	18
913	14	Kota	18
914	15	Kudiya, Melakudi	18
915	16	Kurichchan	18
916	17	Kurumbas	18
917	18	Kurumans	18
918	19	Maha Malasar	18
919	20	Malai Arayan	18
920	21	Malai Pandaram	18
921	22	Malai Vedan	18
922	23	Malakkuravan	18
923	24	Malasar	18
924	25	Malayali	18
925	26	Malayakandi	18
926	27	Mannan	18
927	28	Mudugar, Muduvan	18
928	29	Muthuvan	18
929	30	Pallayan	18
930	31	Palliyan	18
931	32	Palliyar	18
932	33	Paniyan	18
933	34	Sholaga	18
934	35	Toda	18
935	36	Uraly	18
936	2	Adi Dravida	19
937	3	Adi Karnataka	19
938	4	Ajila	19
939	6	Ayyanavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
940	7	Baira	19
941	8	Bakuda	19
942	9	Bandi	19
943	10	Bellara	19
944	11	Bharatar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
945	13	Chalavadi	19
946	14	Chamar, Muchi	19
947	15	Chandala	19
948	16	Cheruman	19
949	17	Devendrakulathan	19
950	18	Dom, Dombara, Paidi, Pano	19
951	19	Domban	19
952	20	Godagali	19
953	21	Godda	19
954	22	Gosangi	19
955	23	Holeya	19
956	24	Jaggali	19
957	25	Jambuvulu	19
958	26	Kadaiyan	19
959	27	Kakkalan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
960	28	Kalladi	19
961	29	Kanakkan, Padanna (in the Nilgiris District)	19
962	30	Karimpalan	19
963	31	Kavara (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
966	34	Kootan, Koodan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
967	35	Kudumban	19
968	36	Kuravan, Sidhanar	19
969	39	Maila	19
970	40	Mala	19
971	41	Mannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
972	42	Mavilan	19
973	43	Moger	19
974	44	Mundala	19
975	45	Nalakeyava	19
976	46	Nayadi	19
977	47	Padannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
978	49	Pallan	19
979	50	Palluvan	19
980	51	Pambada	19
981	52	Panan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
982	53	Panchama	19
983	54	Pannadi	19
984	55	Panniandi	19
985	56	Paraiyan, Parayan, Sambavar	19
986	57	Paravan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
987	58	Pathiyan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
988	59	Pulayan, Cheramar	19
989	60	Puthirai Vannan	19
990	61	Raneyar	19
991	62	Samagara	19
992	63	Samban	19
993	64	Sapari	19
994	65	Semman	19
995	66	Thandan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
996	68	Tiruvalluvar	19
997	69	Vallon	19
998	70	Valluvan	19
999	71	Vannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
1000	72	Vathiriyan	19
1001	73	Velan	19
1002	74	Vetan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District).	19
1003	75	Vettiyan	19
1004	76	Vettuvan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	19
1005	1	Adi Andhra	20
1006	5	Arunthathiyar	20
1007	12	Chakkiliyan	20
1008	37	Madari	20
1009	38	Madiga	20
1010	48	Pagadai	20
1011	67	Thoti	20
1012	391	General	21
1013	42	Attur Kilnad Koravars (Salem, Namakkal, Cuddalore, Villupuram, Ramanathapuram, Sivaganga and Virudhunagar Districts)	22
1014	43	Attur Melnad Koravars (Salem and Namakkal District)	22
1015	44	Appanad Kondayam Kottai Maravar (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts)	22
1016	45	Ambalakarar (Thanjavur, Nagapattinam, Tiruvarur, Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	22
1017	46	Ambalakkarar (Suriyanur, Tiruchirapalli District)	22
1018	47	Boyas (Tiruchirapalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal, Dharmapuri and Krishnagiri Districts)	22
1019	48	Battu Turkas	22
1020	49	C.K. Koravars (Cuddalore and Villupuram Districts)	22
1021	50	Chakkala (Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Madurai, Theni, Dindigul and the Nilgiris Districts)	22
1022	51	Changyampudi Koravars (Vellore and Thiruvannamalai Districts)	22
1023	52	Chettinad Valayars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	22
1024	53	Dombs (Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	22
1025	54	Dobba Koravars (Salem and Namakkal Districts)	22
1026	55	Dommars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	22
1027	56	Donga Boya	22
1028	57	Donga Ur. Korachas	22
1029	58	Devagudi Talayaris	22
1030	59	Dobbai Korachas (Tiruchirapalli, Karur Perambalur and Pudukkottai Districts)	22
1031	60	Dabi Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Vellore and Thiruvannamalai Districts)	22
1032	61	Donga Dasaris (Kancheepuram, Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	22
1033	62	Gorrela Dodda Boya	22
1034	63	Gudu Dasaris	22
1035	64	Gandarvakottai Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Cuddalore and Villupuram Districts)	22
1036	65	Gandarvakottai Kallars (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	22
1037	66	Inji Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1038	67	Jogis (Kancheepuram, Tiruvallur, Chennai, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	22
1039	68	Jambavanodai	22
1040	69	Kaladis (Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	22
1041	70	Kal Oddars (Kancheepuram, Thiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam, Tiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem and Namakkal Districts)	22
1042	71	Koravars (Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Pudukkottai, Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Chennai, Madurai, Theni, Dindigul and The Nilgiris Distrists	22
1043	72	Kalinji Dabikoravars (Thanjavur, Nagapattinam, Tiruvarur and Pudukkottai Districts)	22
1044	73	Kootappal Kallars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1045	74	Kala Koravars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1046	75	Kalavathila Boyas	22
1047	76	Kepmaris (Kancheepuram, Tiruvallur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	22
1048	77	Maravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts)	22
1049	78	Monda Koravars	22
1050	79	Monda Golla (Salem and Namakkal Districts)	22
1051	80	Mutlakampatti (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1052	81	Nokkars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1053	82	Nellorepet Oddars (Vellore and Thiruvannamalai Districts)	22
1054	83	Oddars (Thanjavur, Nagapattinam, Thiruvarur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	22
1055	84	Pedda Boyas (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1056	85	Ponnai Koravars (Vellore and Thiruvannamalai Districts)	22
1057	86	Piramalai Kallars (Sivagangai, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	22
1058	108	Varaganeri Koravars (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1059	87	Periya Suriyur Kallars (Tiruchirapalli, Karur, Perambalur, and Pudukkottai Districts)	22
1060	88	Padayachi (Vellayan Kuppam in Cuddalore District and Tennore in Tiruchirapalli District)	22
1061	93	Sakkaraithamadai Koravars (Vellore and Thiruvannamalai districts)	22
1062	89	Punnan Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1063	92	Salem Uppu Koravars (Salem and Namakkal Districts)	22
1064	109	Vettuva Gounder (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1065	90	Servai (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1066	95	Sooramari Oddars (Salem and Namakkal Districts)	22
1067	91	Salem Melnad Koravars (Madurai, Theni, Dindigul, Coimbatore, Erode, Pudukkottai, Tiruchirapalli, Karur, Perambalur, Salem, Namakkal, Vellore and Thiruvannamalai Districts)	22
1068	94	Saranga Palli Koravars	22
1069	96	Sembanad Maravars (Sivaganga, Virudhunagar and Ramanathapuram Districts)	22
1070	97	Thalli Koravars (Salem and Namakkal Districts)	22
1071	98	Telungapatti Chettis (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1072	101	Uppukoravars or Settipalli Koravars (Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Madurai, Theni, Dindigul, Vellore and Thiruvannamalai Districts)	22
1073	99	Thottia Naickers (Sivaganga, Virudhunagar, Ramanathapuram, Kancheepuram, Tiruvallur, Thanjavur, Nagapattinam, Karur, Tiruchirapalli, Karur, Perambalur. Pudukkottai, Tirunelveli, Thoothukudi, Salem, Namakkal, Vellore, Thiruvannamalai, Coimbatore & Erode Districts)	22
1074	100	Thogamalai Koravars or Kepmaris (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1075	102	Urali Gounders (Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1076	103	Wayalpad or Nawalpeta Korachas	22
1077	106	Vettaikarar (Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	22
1078	104	Vaduvarpatti Koravars (Madurai, Theni, Dindigul, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli, Thoothukudi, Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	22
1079	105	Valayars (Madurai, Theni, Dindigul, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Erode and Coimbatore Districts)	22
1080	107	Vetta koravars (Salem and Namakkal District)	22
1081	391	General	23
1082	1	Agamudayar including Thozhu or Thuluva Vellala	24
1083	2	Agaram Vellan Chettiar	24
1084	3	Alwar, Azhavar and Alavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1085	4	Servai (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	24
1086	5	Nulayar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1087	6	Archakarai Vellala	24
1088	7	Aryavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1089	8	Ayira Vaisyar	24
1090	9	Badagar	24
1091	10	Billava	24
1092	11	Bondil	24
1093	12	Boyas (except Tiruchirappalli, Karur, Perambalur, Pudukkottai, The Nilgiris, Salem, Namakkal and Dharmapuri and Krishnagiri Districts)	24
1094	13	Chakkala (except Sivaganga, Virudhunagar, Ramanathapuram, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Madurai, Theni, Dindigul and The Nilgiris Districts)	24
1095	14	Chavalakarar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1096	15	Chettu or Chetty (including Kottar Chetty, Elur Chetty, Pathira Chetty, Valayal Chetty, Pudukadai Chetty) (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1097	16	Chowdry	24
1098	16B	C.S.I. formerly S.I.U.C. (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1099	17	Donga Dasaris (except Kancheepuram Tiruvallur, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Chennai, Salem and Namakkal Districts)	24
1100	18	Devangar, Sedar	24
1101	19	Dombs (except Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts) Dommars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Vellore and Thiruvannamalai Districts)	24
1102	20	Enadi	24
1103	21	Ezhavathy (in Kanyakumari Districts and Shenkottah Taluk of Tirunelveli District)	24
1104	22	Ezhuthachar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1105	23	Ezhuva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1106	24	Gangavar	24
1107	25	Gavara, Gavarai & Vadugar (Vaduvar) (other than Kamma, Kapu, Balija & Reddi)	24
1108	26	Gounder	24
1109	27	Gowda (including Gammala, Kalali and Anuppa Gounder)	24
1110	28	Hegde	24
1111	29	Idiga	24
1112	30	Illathu Pillaimar, Illuvar, Ezhuvar & Illathar	24
1113	31	Jhetty	24
1114	32	Jogis (except Kancheepuram, Tiruvallur, Madurai, Theni, Dindigul, Cuddalore, Villupuram, Vellore and Thiruvannamalai Districts)	24
1115	33	Kabbera	24
1116	34	Kaikolar, Sengunthar	24
1117	35	Kaladi (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Thanjavur, Nagapattinam, Thiruvarur, Pudukkottai, Tiruchirapalli, Karur and Perambalur Districts)	24
1118	36	Kalari Kurup including Kalari Panicker (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1119	37	Kalingi	24
1120	38	Kallar, Easanattu Kallar, Gandharvakottai Kallars (except Thanjavur, Nagapattinam, Thiruvarur and Pudukkottai Districts)	24
1121	39	Kallar Kula Thondaman	24
1122	40	Kalveli Gounder	24
1123	41	Kambar	24
1124	42	Kammalar or Viswakarma, Viswakarmala (including Thattar, Porkollar, Kannar, Karumar, Kollar, Thacher, Kal Thacher, Kamsala and Viswabrahmin)	24
1125	43	Kani, Kanisu, Kaniyar Panikkar	24
1126	44	Kaniyala Vellalar	24
1127	45	Kannada Saineegar, Kannadiyar (Through out the State) and Dasapalanjika (Coimbatore, Erode and the Nilgiris Districts)	24
1128	46	Kannadiya Naidu	24
1129	47	Karpoora Chettiar	24
1130	48	Karuneegar (Seer Karuneegar, Sri Karuneegar, Sarattu Karuneegar, Kaikatti Karuneegar, Mathuvazhi Kanakkar, Sozhi Kanakkar & Sunnambu Karuneegar)	24
1131	49	Kasukkara Chettiar	24
1132	50	Katesar Pattamkatti	24
1133	51	Kavuthiyar	24
1134	52	Kerala Mudali	24
1135	53	Kharvi	24
1136	54	Khatri	24
1137	55	Kongu Vaishnava	24
1138	56	Kongu Vellalars (including Vellala Gounder, NattuGounder, Narambukatti Gounder, Tirumudi Vellalar, Thondu Vellalar, Pala Gounder, Poosari Gounder, Anuppa Vellala Gounder, Padaithalai, Gounder, Chendalai Gounder, Pavalankatti Vellala Gounder, Palla Vellala Gounder, Sanku Vellala Gounder, & Rathinagiri Gounder)	24
1139	57	Koppala Velama	24
1140	58	Koteyar	24
1141	59	Krishnanvaka (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1142	60	Kudikara Vellalar	24
1143	61	Kudumbi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1144	62	Kuga Vellalar	24
1145	63	Kunchidigar	24
1146	63A	Latin Catholics except Latin Catholic Vannar in Kanyakumari District	24
1147	64	Lambadi	24
1148	65	Lingayat (Jangama)	24
1149	66	Mahratta (NonBrahmin) (including Namadev Mahratta)	24
1150	67	Malayar	24
1151	68	Male	24
1152	69	Maniagar	24
1153	70	Maravars (except Thanjavur, Nagapattinam, Tiruvarur, Pudukkottai, Ramanathapuram, Sivaganga, Virudhunagar, Tirunelveli and Thoothukudi Districts) (including Karumaravars. Appanad Kondayamkottai Maravar (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni and Dindigul Districts) and Sambanad Maravars (except Sivaganga, Virudhunagar and Ramanathapuram Districts)	24
1154	71	Moondrumandai Enbathunalu (84) Ur. Sozhia Vellalar	24
1155	72	Mooppan	24
1156	73	Muthuraja, Muthuracha, Muttiriyar, Mutharaiyar	24
1157	74	Nadar, Shanar & Gramani including Christian Nadar, Christian Shanar and Christian Gramani	24
1158	75	Nagaram	24
1159	76	Naikkar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1160	77	Nangudi Vellalar	24
1161	78	Nanjil Mudali (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1162	79	Odar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1163	80	Odiya	24
1164	81	Oottruvalanattu Vellalar	24
1165	82	O.P.S. Vellalar	24
1166	83	Ovachar	24
1167	84	Paiyur Kotta Vellalar	24
1168	85	Pamulu	24
1169	86	Panar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	24
1170	86A	Pandiya Vellalar	24
1171	87	Omitted	24
1172	88	Kathikarar in Kanyakumari District	24
1173	89	Pannirandam Chettiar or Uthama Chettiar	24
1174	90	Parkavakulam (including Surithimar Nathamar, Malayamar, Moopanar & Nainar)	24
1175	91	Perike (including Perike Balija)	24
1176	92	Perumkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1177	93	Podikara Vellalar	24
1178	94	Pooluva Gounder	24
1179	95	Poraya	24
1180	96	Pulavar (in Coimbatore and Erode Districts)	24
1181	97	Pulluvar or Pooluvar	24
1182	98	Pusala	24
1183	99	Reddy (Ganjam)	24
1184	100	Sadhu Chetty (including Telugu Chetty Twenty four manai Telugu Chetty)	24
1185	101	Sakkaravar or Kavathi (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1186	102	Salivagana	24
1187	103	Saliyar, Padmasaliyar, Pattusaliyar, Pattariyar and Adhaviyar	24
1188	104	Savalakkarar	24
1189	105	Senaithalaivar, Senaikudiyar and IIaivaniar	24
1190	105A	Serakula Vellalar	24
1191	106	Sourashtra (Patnulkarar)	24
1192	107	Sozhia Vellalar (including Sozha Vellalar, Vetrilaikarar, Kodikalkarar and Keeraikarar)	24
1193	108	Srisayar	24
1194	109	Sundaram Chetty	24
1195	110	Thogatta Veerakshatriya	24
1196	111	Tholkollar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1197	112	Tholuva Naicker and Vetalakara Naicker	24
1198	113	Omitted	24
1199	114	Thoriyar	24
1200	115	Ukkirakula Kshatriya Naicker	24
1201	116	Uppara, Uppillia and Sagara	24
1202	117	Urali Gounder (except Tiruchirapalli Karur, Perambalur and Pudukkottai Districts) and Orudaya Gounder or Oorudaya Gounder (in Madurai and Theni, Dindigul, Coimbatore, Erode, Tiruchirapalli, Karur, Perambalur, Pudukkottai, Salem and Namakkal Districts)	24
1203	118	Urikkara Nayakkar	24
1204	118A	Virakodi Vellala	24
1205	119	Vallambar	24
1206	119A	Vallanattu Chettiar	24
1207	120	Valmiki	24
1208	121	Vaniyar, Vania Chettiar (including Gandla, Ganika, Telikula and Chekkalar)	24
1209	122	Veduvar and Vedar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District Where the Community is a Scheduled Castes)	24
1210	123	Veerasaiva (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1211	124	Velar	24
1212	125	Vellan Chettiar	24
1213	126	Veluthodathu Nair (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1214	127	Vokkaligar (including Vakkaligar, Okkaligar, Kappaliyar, Kappiliya, Okkaliga Gowda, Okkaliya- Gowder, Okkaliya-Gowda, Okkaliya Gowda)	24
1215	128	Wynad Chetty (The Nilgiris District)	24
1216	129	Yadhava (including Idaiyar, Telugu Speaking Idaiyar known as Vaduga Ayar or Vaduga Idaiyar or Golla and Asthanthra Golla)	24
1217	130	Yavana	24
1218	131	Yerukula	24
1219	18A	Latin Catholic Christian Vannar	24
1220	12	Oddars (except Thanjavur, Nagapattinam, Thiruvarur, Tiruchirappalli, Karur, Perambalur, Pudukkottai, Madurai, Theni and Dindigul Districts)	24
1221	12	Pedda Boyar (except Tiruchirappalli, Karur, Perambalur and Pudukkottai Districts)	24
1222	63b	Latin Catholics in Shencottah Taluk of Tirunelveli District	24
1223	12	Kaloddars (except Kancheepuram, Tiruvallur, Ramanathapuram, Sivaganga, Virudhunagar, Madurai, Theni, Dindigul, Pudukkottai, Tiruchirappalli, Karur, Perambalur, Tirunelveli, Thoothukudi, Salem & Namakkal Districts)	24
1224	12	Nellorepet Oddars (except Vellore and Thiruvannamalai Districts) Sooramari Oddars (except Salem and Namakkal Districts)	24
1225	12	Sooramari Oddars (except Salem and Namakkal Districts)	24
1226	38	Kottappal Kallars (except Pudukkottai, Tiruchirapalli, Karur and Permbalur Districts)	24
1227	132	Orphans and destitues children who have lost their Parents before reaching the age of ten and are destitutes  and who have nobody else to take care of them either by law or custom  and also who are admitted into any of the Schools or orphanages run by the Government or recognised by the Government.	24
1228	131A	Converts to Christianity from any Hindu Backward Classes Community or Most Backward Classes Community (except the Converts to Christianity from Meenavar, Parvatharajakulam, Pattanavar, Sembadavar, Mukkuvar or Mukayar and Paravar) or Denotified Communities	24
1229	38	Piramalai Kallars (except Sivaganga, Virudhunagar, Ramanathapuram, Madurai, Theni, Dindigul, Pudukkottai, Thanjavur, Nagapattinam and Thiruvarur Districts)	24
1230	38	Periyasooriyur Kallars (except Tiruchirapalli, Karur, Perambalur and Pudukkottai Districts)	24
1231	16A	Converts to Christianity from Scheduled Castes irrespective of the generation of conversion (except the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	24
1232	1	Ambalakarar	25
1233	2	Andipandaram	25
1234	2A	Arayar (in Kanyakumari District)	25
1235	3	Bestha, Siviar	25
1236	4	Bhatraju (Other than Kshatriya Raju)	25
1237	6	Dasari	25
1238	7	Dommara	25
1239	8	Eravallar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Tribe)	25
1240	9	Isaivellalar	25
1241	10	Jambuvanodai	25
1242	11	Jangam	25
1243	12	Jogi	25
1244	13	Kongu Chettiar (in Coimbatore and Erode Districts only)	25
1245	14	Koracha	25
1246	15	Kulala (including Kuyavar and Kumbarar)	25
1247	16	Kunnuvar Mannadi	25
1248	17	Kurumba, Kurumba Goundar	25
1249	18	Kuruhini Chetty	25
1250	19	Maruthuvar, Navithar, Mangala, Velakattalavar, Velakatalanair and Pronopakari	25
1251	20	Mond Golla	25
1252	21	Moundadan Chetty	25
1253	22	Mahendra, Medara	25
1254	23	Mutlakampatti	25
1255	24	Narikoravar (Kuruvikars)	25
1256	25	Nokkar	25
1257	25A	Panisaivan / Panisivan	25
1258	26	Vanniakula Kshatriya (including Vanniyar, Vanniya, Vannia Gounder, Gounder or Kander, Padayachi, Palli & Agnikula Kshatriya)	25
1259	27	Paravar (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is Scheduled Caste)	25
1260	27A	Paravar converts to Christianity including the Paravar converts to Christianity of Kanyakumari District and Shenkottah Taluk in Tirunelveli District)	25
1261	28	Meenavar (Parvatharajakulam, Pattanavar, Sembadavar) (including converts to Christianity)	25
1262	29	Mukkuvar or Mukayar (including converts to Christianity)	25
1263	30	Punnan Vettuva Gounder	25
1264	31	Pannayar (other than Kathikarar in Kanyakumari District)	25
1265	32	Sathatha Srivaishnava (including Sathani, Chattadi and Chattada Srivaishnava)	25
1266	33	Sozhia Chetty	25
1267	34	Telugupatty Chetty	25
1268	35	Thottia Naicker (including Rajakambalam, Gollavar, Sillavar, Thockalavar, Thozhuva Naicker and Erragollar)	25
1269	36	Thondaman	25
1270	36A	Thoraiyar (Nilgiris)	25
1271	36B	Thoraiyar (Plains)	25
1272	37	Valaiyar (including Chettinad Valayars)	25
1273	38	Vannar (Salaivai Thozhilalar) (including Agasa, Madivala, Ekali, Rajakula, Veluthadar & Rajaka) (except in Kanyakumari District and Shenkottah Taluk of Tirunelveli District where the Community is a Scheduled Caste)	25
1274	39	Vettaikarar	25
1275	40	Vettuva Gounder	25
1276	41	Yogeeswarar	25
1277	5	Boyar, Oddar	25
1278	18A	Latin Catholic Christian Vannar (in Kanyakumari District)	25
1279	36C	Transgender or Eunuch (Thirunangai or Aravani)	25
1280	2	Adi Dravida	26
1281	3	Adi Karnataka	26
1282	4	Ajila	26
1283	6	Ayyanavar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1284	7	Baira	26
1285	8	Bakuda	26
1286	9	Bandi	26
1287	10	Bellara	26
1288	11	Bharatar (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1289	13	Chalavadi	26
1290	14	Chamar, Muchi	26
1291	15	Chandala	26
1292	16	Cheruman	26
1293	17	Devendrakulathan	26
1294	18	Dom, Dombara, Paidi, Pano	26
1295	19	Domban	26
1296	20	Godagali	26
1297	21	Godda	26
1298	22	Gosangi	26
1299	23	Holeya	26
1300	24	Jaggali	26
1301	25	Jambuvulu	26
1302	26	Kadaiyan	26
1303	27	Kakkalan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1304	28	Kalladi	26
1305	29	Kanakkan, Padanna (in the Nilgiris District)	26
1306	30	Karimpalan	26
1307	31	Kavara (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1308	32	Koliyan	26
1309	33	Koosa	26
1310	34	Kootan, Koodan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1311	35	Kudumban	26
1312	36	Kuravan, Sidhanar	26
1313	39	Maila	26
1314	40	Mala	26
1315	41	Mannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1316	42	Mavilan	26
1317	43	Moger	26
1318	44	Mundala	26
1319	45	Nalakeyava	26
1320	46	Nayadi	26
1321	47	Padannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1322	49	Pallan	26
1323	50	Palluvan	26
1324	51	Pambada	26
1325	52	Panan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1326	53	Panchama	26
1327	54	Pannadi	26
1328	55	Panniandi	26
1329	56	Paraiyan, Parayan, Sambavar	26
1330	57	Paravan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1331	58	Pathiyan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1332	59	Pulayan, Cheramar	26
1333	60	Puthirai Vannan	26
1334	61	Raneyar	26
1335	62	Samagara	26
1336	63	Samban	26
1337	64	Sapari	26
1338	65	Semman	26
1339	66	Thandan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1340	68	Tiruvalluvar	26
1341	69	Vallon	26
1342	70	Valluvan	26
1343	71	Vannan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1344	72	Vathiriyan	26
1345	73	Velan	26
1346	74	Vetan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District).	26
1347	75	Vettiyan	26
1348	76	Vettuvan (in Kanyakumari District and Shenkottah Taluk of Tirunelveli District)	26
1349	391	General	27
\.


--
-- Name: baseapp_sub_castes_pkey; Type: CONSTRAINT; Schema: public; Owner: emisf13; Tablespace: 
--

ALTER TABLE ONLY baseapp_sub_castes
    ADD CONSTRAINT baseapp_sub_castes_pkey PRIMARY KEY (id);


--
-- Name: baseapp_sub_castes_community_id; Type: INDEX; Schema: public; Owner: emisf13; Tablespace: 
--

CREATE INDEX baseapp_sub_castes_community_id ON baseapp_sub_castes USING btree (community_id);


--
-- Name: baseapp_sub_castes_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: emisf13
--

ALTER TABLE ONLY baseapp_sub_castes
    ADD CONSTRAINT baseapp_sub_castes_community_id_fkey FOREIGN KEY (community_id) REFERENCES baseapp_community(id);


--
-- PostgreSQL database dump complete
--

