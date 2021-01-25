SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.account (
    id integer NOT NULL
);


ALTER TABLE public.account OWNER TO postgres;

ALTER TABLE public.account ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.commodity (
    id integer NOT NULL
);


ALTER TABLE public.commodity OWNER TO postgres;

ALTER TABLE public.commodity ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.commodity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.entry (
    id integer NOT NULL,
    account integer NOT NULL,
    change numeric(18,4) NOT NULL,
    commodity1 integer NOT NULL,
    converted numeric(18,4) NOT NULL,
    commodity2 integer NOT NULL,
    transaction integer NOT NULL
);


ALTER TABLE public.entry OWNER TO postgres;

ALTER TABLE public.entry ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.transaction (
    id integer NOT NULL
);


ALTER TABLE public.transaction OWNER TO postgres;

ALTER TABLE public.transaction ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.commodity
    ADD CONSTRAINT commodity_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);

CREATE INDEX fki_account ON public.entry USING btree (account);

CREATE INDEX fki_commodity ON public.entry USING btree (commodity1);

CREATE INDEX fki_entry_currency_fkey ON public.entry USING btree (commodity2);

CREATE INDEX fki_transaction ON public.entry USING btree (transaction);

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_account_fkey FOREIGN KEY (account) REFERENCES public.account(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_commodity_fkey FOREIGN KEY (commodity1) REFERENCES public.commodity(id) NOT VALID;

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_currency_fkey FOREIGN KEY (commodity2) REFERENCES public.commodity(id) NOT VALID;

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_transaction_fkey FOREIGN KEY (transaction) REFERENCES public.transaction(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
