<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

  <xsl:template name="figure" match="figure" mode="call-template">
  <img
            src="https://cooperacion.us.es/sites/default/files/GENERAL/US_VSSyC-OCD_color.png"
            class="h-12 my-5"
            id="{@id}"
        />
    
        
  </xsl:template>

</xsl:stylesheet>