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
-- Name: baseapp_religion; Type: TABLE; Schema: public; Owner: emisf13; Tablespace: 
--

CREATE TABLE baseapp_religion (
    id integer NOT NULL,
    religion_name character varying(100) NOT NULL
);


ALTER TABLE public.baseapp_religion OWNER TO emisf13;

--
-- Name: baseapp_religion_id_seq; Type: SEQUENCE; Schema: public; Owner: emisf13
--

CREATE SEQUENCE baseapp_religion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.baseapp_religion_id_seq OWNER TO emisf13;

--
-- Name: baseapp_religion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: emisf13
--

ALTER SEQUENCE baseapp_religion_id_seq OWNED BY baseapp_religion.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: emisf13
--

ALTER TABLE ONLY baseapp_religion ALTER COLUMN id SET DEFAULT nextval('baseapp_religion_id_seq'::regclass);


--
-- Data for Name: baseapp_religion; Type: TABLE DATA; Schema: public; Owner: emisf13
--

COPY baseapp_religion (id, religion_name) FROM stdin;
1	Hindu
2	Christian
3	Muslim
5	Jainism
6	Sikh
4	others
\.


--
-- Name: baseapp_religion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: emisf13
--

SELECT pg_catalog.setval('baseapp_religion_id_seq', 4, true);


--
-- Name: baseapp_religion_pkey; Type: CONSTRAINT; Schema: public; Owner: emisf13; Tablespace: 
--

ALTER TABLE ONLY baseapp_religion
    ADD CONSTRAINT baseapp_religion_pkey PRIMARY KEY (id);


--
-- Name: baseapp_religion; Type: ACL; Schema: public; Owner: emisf13
--

REVOKE ALL ON TABLE baseapp_religion FROM PUBLIC;
REVOKE ALL ON TABLE baseapp_religion FROM emisf13;
GRANT ALL ON TABLE baseapp_religion TO emisf13;
GRANT ALL ON TABLE baseapp_religion TO postgres;


--
-- Name: baseapp_religion_id_seq; Type: ACL; Schema: public; Owner: emisf13
--

REVOKE ALL ON SEQUENCE baseapp_religion_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE baseapp_religion_id_seq FROM emisf13;
GRANT ALL ON SEQUENCE baseapp_religion_id_seq TO emisf13;
GRANT ALL ON SEQUENCE baseapp_religion_id_seq TO postgres;


--
-- PostgreSQL database dump complete
--

