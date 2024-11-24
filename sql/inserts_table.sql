/* INSERT DE CARROS /
INSERT INTO DBAUTOCAR.CARROS VALUES(ID, 'ONIX', 2024,'CHEVROLET', TRUE);
INSERT INTO DBAUTOCAR.CARROS VALUES(ID, 'LANCER', 2023,'MITSUBISHI', TRUE);
INSERT INTO DBAUTOCAR.CARROS VALUES(ID, 'COROLLA', 2024,'TOYOTA', TRUE);
INSERT INTO DBAUTOCAR.CARROS VALUES(ID, 'CIVIC', 2024,'HONDA', TRUE);
INSERT INTO DBAUTOCAR.CARROS VALUES(ID, 'ARGO', 2024,'FIAT', TRUE);

/ INSERT DE CLIENTES /
SELECT FROM CLIENTES;
INSERT INTO DBAUTOCAR.CLIENTES VALUES(ID, 'GUSTAVO', "34583479410","1234 1234 5467 9004", "(27)99345-4423", 'exemplo@hotmail.com');
INSERT INTO DBAUTOCAR.CLIENTES VALUES(ID, 'MARLON', "29567839561","3123 4564 5237 9494", "(27)99123-9932", 'exempl2@hotmail.com');
INSERT INTO DBAUTOCAR.CLIENTES VALUES(ID, 'LUCAS', "38604345860","1234 1234 5467 5454", "(27)99894-2345", 'exemplo3@hotmail.com');
INSERT INTO DBAUTOCAR.CLIENTES VALUES(ID, 'NICHOLE', "53455533456","4909 2134 5467 9634", "(27)98989-3254", 'exemplo22@hotmail.com');
INSERT INTO DBAUTOCAR.CLIENTES VALUES(ID, 'FABRICIO', "86493068102","2345 2987 5556 1430", "(27)98989-3254", 'exemplo22@hotmail.com');

/INSERT LOCACAO - este insert é para a tabela de locacao, trocar o que está em parênteses para os valores corretos/
SELECT * FROM LOCACAO;

INSERT INTO DBAUTOCAR.LOCACAO VALUES(ID, (colocar id_carro), (colocar id_cliente), (Data_locacao), (Data_retorno), (Valor_diaria);