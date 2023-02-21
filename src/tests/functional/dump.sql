--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE auth_database_tests;




--
-- Drop roles
--

DROP ROLE app;


--
-- Roles
--

CREATE ROLE app;
ALTER ROLE app WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md5c9377313baea21e871f6c06c4e62810d';






--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-1.pgdg110+1)
-- Dumped by pg_dump version 13.10 (Debian 13.10-1.pgdg110+1)

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

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: app
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO app;

\connect template1

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
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: app
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: app
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

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
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: app
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- Database "auth_database_tests" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-1.pgdg110+1)
-- Dumped by pg_dump version 13.10 (Debian 13.10-1.pgdg110+1)

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
-- Name: auth_database_tests; Type: DATABASE; Schema: -; Owner: app
--

CREATE DATABASE auth_database_tests WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE auth_database_tests OWNER TO app;

\connect auth_database_tests

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO app;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.roles (
    id uuid NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    created timestamp without time zone NOT NULL,
    modified timestamp without time zone NOT NULL
);


ALTER TABLE public.roles OWNER TO app;

--
-- Name: user_history; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.user_history (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    action character varying NOT NULL,
    user_agent character varying NOT NULL,
    created timestamp without time zone NOT NULL
);


ALTER TABLE public.user_history OWNER TO app;

--
-- Name: users; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    is_admin boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    modified timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO app;

--
-- Name: users_roles; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.users_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);


ALTER TABLE public.users_roles OWNER TO app;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.alembic_version (version_num) FROM stdin;
5c5f6543a680
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.roles (id, name, description, created, modified) FROM stdin;
4cd6adcd-abf9-44e6-90a9-65f32782d25d	Licensed conveyancer	Catch well break imagine.\nOfficial rise source. Site democratic imagine argue activity. Fire story certain region street.\nTheir level few bar fine. Child beyond born yes remember land particularly.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
58eeb22b-282a-460b-914b-b37550fb61df	Field seismologist	Certain city visit close somebody trade art factor. Bank career scientist as many. Professor by send resource certain suggest little travel. Home design industry name.	2023-02-21 15:43:58.363394	2023-02-21 15:43:58.363479
317dc742-7656-48e8-ace5-c3eb0da2cffb	Air cabin crew	Arm player follow leader her. Strong past officer lead.\nPick yourself although lose practice. For probably hard lawyer agreement building behind. A memory possible health.	2023-02-21 15:43:58.363394	2023-02-21 15:43:58.363479
a7e42e5d-4d64-4c1f-be87-18100035684f	Site engineer	In affect above soldier have southern seem. Nor north ahead interview per.\nReason staff measure.	2023-02-21 15:43:58.363394	2023-02-21 15:43:58.363479
3a3b1dbe-44f8-4a01-8aec-6a8d5c685a16	Chief Financial Officer	Great name concern lose mission financial though. Democratic something trip share building feel discuss.	2023-02-21 15:43:58.363394	2023-02-21 15:43:58.363479
40d948ac-409f-4ffb-b9d1-3dae31e066cd	Private music teacher	Check argue enough physical challenge home myself. Treatment peace price daughter per sit newspaper.\nOld ability style daughter common of more. Best long other door call.	2023-02-21 15:43:58.412062	2023-02-21 15:43:58.412134
b49e54c5-19a5-410a-ba08-355dd603abcb	Facilities manager	Now job share political.\nRemember arm guy discussion focus read. Lawyer industry travel phone any personal away.\nWrite minute dark safe air your. Clearly as defense create service lay.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
e564dde5-6ee6-44e4-9dd9-0858fb81548e	Restaurant manager	Call up until brother. Almost instead room say. Summer mind community particular. True reduce until good still within actually.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
6986a29c-44f6-488b-bc50-d64622ca0ad0	Interior and spatial designer	Time matter rise PM listen compare.\nReflect company without would loss site seek on. Green really sister hand past nice cause.\nForm which benefit full serve make.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
ca60e246-bc8d-40e1-a74f-48d0cd9d93ed	Actuary	All garden performance include. Put here newspaper say.\nForm simple strong behind detail watch.\nHis catch tonight thought. Join through who develop pattern.\nAddress never already environment.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
b21b1f16-96d4-4521-a193-e35ccaac93f5	Marketing executive	Government eat course remain phone share push. Land cut guess my. Series person either prepare responsibility both especially. Investment small he mean account.	2023-02-21 15:43:58.329873	2023-02-21 15:43:58.329973
\.


--
-- Data for Name: user_history; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.user_history (id, user_id, action, user_agent, created) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.users (id, email, password, is_admin, created, modified) FROM stdin;
1a99b6f3-65d8-454c-86f8-05455fb7d000	gtran@example.com	pbkdf2:sha256:260000$Cyx7Hb7Wb5xXJ74L$e345660598292a18a88a42b3041d7a8379cdd9da586f965b071f192f0a32732c	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
7d81309f-2345-40e9-8c71-ece70cd0e830	kingtravis@example.org	pbkdf2:sha256:260000$X1asw1xBhIS2t9de$c4ee69ca736e4cec4ce160da4238612182ace91fef9c6ed89c8dfe665c48bfee	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
f0f444ac-4cf6-4354-9374-ebaa6dd1e18f	uallen@example.net	pbkdf2:sha256:260000$jW2X9T0PKWF8ZEmP$f9c84627682323b352beb876b5429de14b40e800b0dacd916298d4b880a127cb	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
a408285c-0a12-4803-a319-c8bd0caf5c43	christophercarlson@example.org	pbkdf2:sha256:260000$Jl2IxqPw5q09zHPo$283b60c26f6090b4cc54fd49d665409851ebc2139da9a3327e9d511de450967c	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
8c4eeb7b-a1f2-48ba-b004-6c2cb9bae4aa	owells@example.com	pbkdf2:sha256:260000$EKjcN1enxLkCwqds$65c32f56fd370c7c21770d8a46108014e619b2f5d29aa6a9701296830617538d	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
01903028-8191-4f6c-a759-f659ac87ddf0	andersonbrittany@example.net	pbkdf2:sha256:260000$vQgOFPl7xHnbhWDa$b30acacb2f7bbc0f0c877d0244d1d5d60032d1369d58b0042ab278645cfef449	f	2023-02-21 15:43:58.366595	2023-02-21 15:43:58.366619
5e2630f0-a73f-42e7-883d-271494623794	melendezbrian@example.com	pbkdf2:sha256:260000$cQgOhet7u63cYLzv$3d1b793bfa59903d8752c7428e43578cb52ccb0d624638bd32fc88c3b1d4a8be	f	2023-02-21 15:43:58.333224	2023-02-21 15:43:58.33325
c2d7d0c2-fe2b-4720-8fb8-1fd057a832ca	ysmith@example.net	pbkdf2:sha256:260000$c1EGJUvMrPZP5sSy$af680d618d5a3ad5655710febc0795f7cd96c5ae0924e1f61e9ab854987dfcca	f	2023-02-21 15:43:58.333224	2023-02-21 15:43:58.33325
a9156262-9ee2-4b60-9de2-af4600bb2e8e	jenniferedwards@example.com	pbkdf2:sha256:260000$fRLIhElTRZaCYwdk$05653d743d5279c290e656484e0ca459400e19d1b7a23cd5c3aa0795021cef9d	f	2023-02-21 15:43:58.333224	2023-02-21 15:43:58.33325
ea08eb76-b03d-494b-9186-f3e1722c8af9	travis58@example.com	pbkdf2:sha256:260000$xmFJRKq8nw7ON2oK$1f31f0090e9e1802a9182d8063ae946568b97d4b2eb1bb8fd40f04da694684c2	f	2023-02-21 15:43:58.366595	2023-02-21 15:43:58.366619
503743d1-cfde-42c5-8dca-249849eb9a5c	kimberly52@example.org	pbkdf2:sha256:260000$ibwT96VdNlsmtOdL$80a608e15130f38cac1369d47f3545423f0cec1ac3950e6c6d9bcd7c264f0f49	f	2023-02-21 15:43:58.315268	2023-02-21 15:43:58.315294
0f623d7c-5e57-405c-900f-d9f61a5a8305	admin@admin.com	pbkdf2:sha256:260000$XuX3rfsgARiWcFH4$3d48648fce95fad496facbc94211f37536d8e3290068c8d8db7d8645fef79d99	t	2023-02-21 15:43:58.366595	2023-02-21 15:43:58.366619
8f122ab1-607a-4227-89e6-07ac15ee1f27	user@user.com	pbkdf2:sha256:260000$0PgjUma0Sj7RBn5C$60fbd429e4c9bf0edd1bd457f982f12c84322dae4d32a4dd7f19b83ac458c614	f	2023-02-21 15:43:58.333224	2023-02-21 15:43:58.33325
\.


--
-- Data for Name: users_roles; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.users_roles (user_id, role_id) FROM stdin;
1a99b6f3-65d8-454c-86f8-05455fb7d000	4cd6adcd-abf9-44e6-90a9-65f32782d25d
7d81309f-2345-40e9-8c71-ece70cd0e830	58eeb22b-282a-460b-914b-b37550fb61df
c2d7d0c2-fe2b-4720-8fb8-1fd057a832ca	317dc742-7656-48e8-ace5-c3eb0da2cffb
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: user_history user_history_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_roles users_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: user_history user_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.user_history
    ADD CONSTRAINT user_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users_roles users_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: users_roles users_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT users_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-1.pgdg110+1)
-- Dumped by pg_dump version 13.10 (Debian 13.10-1.pgdg110+1)

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

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: app
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO app;

\connect postgres

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
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: app
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

