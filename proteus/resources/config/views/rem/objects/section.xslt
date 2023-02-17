<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

<xsl:template name="section" match="section" mode="call-template">
    <h2 id="{@id}" class="text-2xl text-blue-900 my-5" contenteditable="false">
        <xsl:value-of select="properties/*[@name='name']" disable-output-escaping="yes"/>
    </h2>
</xsl:template>
</xsl:stylesheet>