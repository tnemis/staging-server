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
-- Name: baseapp_community; Type: TABLE; Schema: public; Owner: emisf13; Tablespace: 
--

CREATE TABLE baseapp_community (
    id integer NOT NULL,
    community_code character varying(30) NOT NULL,
    community_name character varying(30) NOT NULL,
    religion_id integer NOT NULL
);


ALTER TABLE public.baseapp_community OWNER TO emisf13;

--
-- Data for Name: baseapp_community; Type: TABLE DATA; Schema: public; Owner: emisf13
--

COPY baseapp_community (id, community_code, community_name, religion_id) FROM stdin;
1	BC-Others	BC-Others	1
2	BC-Muslim	BC-Muslim	3
3	MBC	MBC	1
4	ST	ST	1
5	SC-Others	SC-Others	1
6	SC-Arunthathiyar	SC-Arunthathiyar	1
8	OC	OC	1
9	DNC	DNC (Denotified Communities)	1
10	BC-Others	BC-Others	2
11	MBC	MBC	2
12	OC	OC	2
13	DNC	DNC (Denotified Communities)	2
14	ST	ST	2
15	OC	OC	3
16	BC-Others	BC-Others	4
17	MBC	MBC	4
18	ST	ST	4
19	SC-Others	SC-Others	4
20	SC-Arunthathiyar	SC-Arunthathiyar	4
21	OC	OC	4
22	DNC	DNC (Denotified Communities)	4
23	OC	OC	5
24	BC-Others	BC-Others	6
25	MBC	MBC	6
26	SC-Others	SC-Others	6
27	OC	OC	6
\.


--
-- Name: baseapp_community_pkey; Type: CONSTRAINT; Schema: public; Owner: emisf13; Tablespace: 
--

ALTER TABLE ONLY baseapp_community
    ADD CONSTRAINT baseapp_community_pkey PRIMARY KEY (id);


--
-- Name: baseapp_community_religion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: emisf13
--

ALTER TABLE ONLY baseapp_community
    ADD CONSTRAINT baseapp_community_religion_id_fkey FOREIGN KEY (religion_id) REFERENCES baseapp_religion(id);


--
-- PostgreSQL database dump complete
--

