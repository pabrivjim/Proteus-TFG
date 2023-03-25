<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>
  <xsl:template match="paragraph" name="paragraph">
    <xsl:value-of name="pString" select="proteus:markdown(properties/*[@name='description'])" disable-output-escaping="yes"/>
  </xsl:template>
</xsl:stylesheet>
