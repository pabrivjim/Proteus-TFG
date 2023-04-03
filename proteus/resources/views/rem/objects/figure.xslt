<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

  <xsl:template name="figure" match="figure" mode="call-template">
    <xsl:choose>
      <!-- If the image has the position property then we justify it depending on the value of the property -->
      <xsl:when test="properties/*[@name='position']">
        <xsl:choose>
          <xsl:when test="properties/*[@name='position']='left'">
            <xsl:call-template name="filter"/>
          </xsl:when>
          <xsl:when test="properties/*[@name='position']='center'">
            <div class="flex justify-center">
              <xsl:call-template name="filter"/>
            </div>
          </xsl:when>
          <xsl:when test="properties/*[@name='position']='right'">
            <div class="flex justify-end">
              <xsl:call-template name="filter"/>
            </div>
          </xsl:when>
        </xsl:choose>
      </xsl:when>
      <!-- If there is no property position, then we just show the image -->
      <xsl:otherwise>
        <xsl:call-template name="filter" />
      </xsl:otherwise>
    </xsl:choose>
        
  </xsl:template>
  
  <!-- This template is called by the figure template and it shows the image with the filter if it has the filter property -->
  <xsl:template name="filter" mode="call-template">
    <xsl:choose>
      <xsl:when test="properties/*[@name='filter']='black'">
        <img
                src="{proteus:black('https://cooperacion.us.es/sites/default/files/GENERAL/US_VSSyC-OCD_color.png')}"
                class="h-12 my-5"
                id="{@id}"/>
      </xsl:when>
      <xsl:otherwise>
        <img
                src="https://cooperacion.us.es/sites/default/files/GENERAL/US_VSSyC-OCD_color.png"
                class="h-12 my-5"
                id="{@id}"/> 

      </xsl:otherwise>
    </xsl:choose>
    </xsl:template>

</xsl:stylesheet>