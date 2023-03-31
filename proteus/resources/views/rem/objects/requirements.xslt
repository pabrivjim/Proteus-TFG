<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>
  <xsl:template match="requirements" name="requirements">
  <!-- <xsl:param name="@classes"/> -->
  <!-- We want the format as #### -->
  <!-- <xsl:value-of select="format-number($i, '0000')"/> -->
    <div class="border-4 border-blue-300 my-5">
      <h5 class="bg-blue-200 p-1 {@classes}">
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

            <!-- We add the preCondition because Use of case have them. -->
            <xsl:with-param name="preCondition">
                <xsl:value-of select="properties/*[@name='preCondition']"/>
            </xsl:with-param>
            <xsl:with-param name="stability">
                <xsl:value-of select="properties/*[@name='stability']"/>
            </xsl:with-param>
            <xsl:with-param name="developmentState">
                <xsl:value-of select="properties/*[@name='developmentState']"/>
            </xsl:with-param>
            <xsl:with-param name="urgency">
                <xsl:value-of select="properties/*[@name='urgency']"/>
            </xsl:with-param>
            <xsl:with-param name="postCondition">
                <xsl:value-of select="properties/*[@name='postCondition']"/>
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


