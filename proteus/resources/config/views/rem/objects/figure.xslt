<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

  <xsl:template name="figure" match="figure" mode="call-template">
    <div id="{@id}" contenteditable="false">
      <xsl:variable name="image" select="properties/*[@name='url']"/>
      <xsl:value-of select="$image" disable-output-escaping="yes"/>
      <img src="$image"/>
    </div>
        
  </xsl:template>

</xsl:stylesheet>