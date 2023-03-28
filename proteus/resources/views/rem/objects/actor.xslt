<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>
  <xsl:template match="actor" name="actor">
    <div class="border-4 border-blue-300 my-5">
      <h5 class="bg-blue-200 p-1">
        <span class="secno">
          <xsl:value-of select="properties/*[@name='identifier']"/>
        </span>
      </h5>
      <div class="summary">
        <table class="m-3">
          <tbody class="text-left">
           <xsl:call-template name="proteus_table">
            <xsl:with-param name="version">
                <xsl:value-of select="concat(properties/*[@name='version'], ' (' , properties/*[@name='date'], ')')"/>
            </xsl:with-param>
            <xsl:with-param name="description">
                <xsl:value-of select="properties/*[@name='description']"/>
            </xsl:with-param>
            <xsl:with-param name="comments">
                <xsl:value-of select="properties/*[@name='comments']"/>
            </xsl:with-param>
            </xsl:call-template>
          </tbody>
        </table>
      </div>
    </div>
  </xsl:template>

</xsl:stylesheet>


