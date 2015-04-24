/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_cdrport` BEFORE INSERT ON `cdr_cdr` FOR EACH ROW BEGIN


DROP TEMPORARY TABLE IF EXISTS TMP_cdr_cdr;

CREATE TEMPORARY TABLE `TMP_cdr_cdr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `calldate` datetime NOT NULL,
  `clid` varchar(80) NOT NULL,
  `src` varchar(80) NOT NULL,
  `dst` varchar(80) NOT NULL,
  `dcontext` varchar(80) NOT NULL,
  `channel` varchar(80) NOT NULL,
  `dstchannel` varchar(80) NOT NULL,
  `lastapp` varchar(80) NOT NULL,
  `lastdata` varchar(80) NOT NULL,
  `duration` int(11) NOT NULL,
  `billsec` int(11) NOT NULL,
  `disposition` varchar(45) NOT NULL,
  `amaflags` int(11) NOT NULL,
  `accountcode` varchar(20) NOT NULL,
  `uniqueid` varchar(32) NOT NULL,
  `userfield` varchar(255) NOT NULL,
  `prefix` varchar(80) DEFAULT NULL,
  `portado` varchar(3) DEFAULT 'Nao',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;

INSERT INTO TMP_cdr_cdr (calldate,clid,src,dst,dcontext,channel,dstchannel,lastapp,lastdata,duration,billsec,disposition,amaflags,accountcode,uniqueid,userfield,prefix,portado)
SELECT calldate,clid,src,dst,dcontext,channel,dstchannel,lastapp,lastdata,duration,billsec,disposition,amaflags,accountcode,uniqueid,userfield,prefix,`portado`
FROM cdr_cdr;

	UPDATE TMP_cdr_cdr SET prefix = 
		CASE
			WHEN dst LIKE '%s-%'
				THEN src
			WHEN dst LIKE '%-%'
				THEN src
			WHEN character_length(dst)='10'
				THEN SUBSTRING(dst,1,6)
			WHEN character_length(dst)='11'
				THEN SUBSTRING(dst,1,7)
			WHEN character_length(dst)<'9'
				THEN src
		END;

UPDATE TMP_cdr_cdr
	INNER JOIN portados
		ON TMP_cdr_cdr.dst = portados.numero
	SET portado = 
		CASE
			WHEN TMP_cdr_cdr.dst = portados.numero
				THEN 'Sim'
		END;

INSERT INTO cdr_cdrport (calldate,src,dst,duration,billsec,disposition,ddd,prefixo,cidade,estado,operadora,tipo,rn1,portado,uniqueid)
SELECT calldate,src,dst,SEC_TO_TIME(duration) AS duration, SEC_TO_TIME(billsec) AS billsec,disposition,cdr_prefixo.ddd,
		cdr_prefixo.prefixo,cdr_prefixo.cidade,cdr_prefixo.estado,cdr_prefixo.operadora,cdr_prefixo.tipo, cdr_prefixo.rn1, portado,uniqueid 
	FROM TMP_cdr_cdr,cdr_prefixo
	WHERE TMP_cdr_cdr.prefix = cdr_prefixo.prefixo
	ON DUPLICATE KEY UPDATE uniqueid = cdr_cdrport.uniqueid;


END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = latin1 */ ;;
/*!50003 SET character_set_results = latin1 */ ;;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `atualiza_base` ON SCHEDULE EVERY 1 MINUTE STARTS '2015-04-20 17:47:46' ON COMPLETION PRESERVE ENABLE DO BEGIN
	UPDATE cdr_cdr SET prefix = 
		CASE
			WHEN dst LIKE '%s-%'
				THEN src
			WHEN character_length(dst)='10'
				THEN SUBSTRING(dst,1,6)
			WHEN character_length(dst)='11'
				THEN SUBSTRING(dst,1,7)
			WHEN character_length(dst)<'9'
				THEN src
		END;

END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = latin1 */ ;;
/*!50003 SET character_set_results = latin1 */ ;;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `Stats` ON SCHEDULE EVERY 5 MINUTE STARTS '2015-04-24 10:43:12' ON COMPLETION PRESERVE ENABLE DO BEGIN
TRUNCATE TABLE cdr_dispositionpercent;
ALTER TABLE cdr_dispositionpercent AUTO_INCREMENT = 1;
REPLACE INTO cdr_dispositionpercent (disposition, valor, perc)	
	SELECT lista.disposition, total valor , 
	        ((total / total.total_geral) * 100) perc
		FROM
		(
		SELECT disposition, total
			FROM vw_disposition) lista,
		(
		SELECT sum(total) total_geral
			FROM vw_disposition
		) total;

END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
