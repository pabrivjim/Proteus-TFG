<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>
  
   <xsl:template match="paragraph" name="paragraph">
        <xsl:param name="pString" select="properties/*[@name='comments']"/>
        <xsl:if test="$pString != '' and $pString !='&#xa;'">
            <xsl:choose>
                <xsl:when test="starts-with($pString,'#')">
                    <xsl:call-template name="header">
                        <xsl:with-param name="pString"
                        select="substring($pString,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="starts-with($pString,'&#xA;')">
                    <xsl:call-template name="list">
                        <xsl:with-param name="pString"
                        select="substring($pString,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="starts-with($pString,'- ')">
                    <xsl:call-template name="listItem">
                        <xsl:with-param name="pString"
                        select="$pString"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                <xsl:call-template name="separator">
                        <xsl:with-param name="pString"
                        select="$pString"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
  </xsl:template>
  <xsl:template name="separator">
    <!-- If there is any new line, it gets the first part and send it to paragraph2 template and the rest to paragraph template.
         This is basically need it because we don't want to show twice for example the information of a list in a string and then again in a list -->
    <xsl:param name="pString"/>
    <xsl:choose>
      <xsl:when test="contains($pString, '&#xA;')">
        <xsl:call-template name="paragraph2">
            <xsl:with-param name="pString"
                            select="substring-before($pString,'&#xA;')"/>
        </xsl:call-template>
        <xsl:call-template name="paragraph">
           <xsl:with-param name="pString"
                           select="substring-after($pString,'&#xA;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="paragraph2">
          <xsl:with-param name="pString"
                          select="$pString"/>
         </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
    <xsl:template name="header">
        <xsl:param name="pString"/>
        <xsl:variable name="vInside"
        select="substring-before($pString,'#&#xA;')"/>
        <xsl:choose>
            <xsl:when test="$vInside != ''">
                <h1>
                    <xsl:call-template name="inline">
                        <xsl:with-param name="pString" select="$vInside"/>
                    </xsl:call-template>
                </h1>
                <xsl:call-template name="paragraph">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,'#&#xA;')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="paragraph2">
                    <xsl:with-param name="pString" 
                                     select="concat('#',$pString)"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="list">
        <xsl:param name="pString"/>
        <xsl:variable name="vCheckList" select="starts-with($pString,'- ')"/>
        <xsl:choose>
            <xsl:when test="$vCheckList">
                <ul class="ml-3">
                    <xsl:call-template name="listItem">
                        <xsl:with-param name="pString" select="$pString"/>
                    </xsl:call-template>
                </ul>
                <xsl:call-template name="paragraph">
                    <xsl:with-param name="pString">
                        <xsl:call-template name="afterlist">
                            <xsl:with-param name="pString" select="$pString"/>
                        </xsl:call-template>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="paragraph">
                    <xsl:with-param name="pString" select="$pString"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="paragraph2">
        <xsl:param name="pString"/>
        <xsl:choose>
        <!-- If the String contains # -->
            <xsl:when test="contains($pString,'# ')">
              <xsl:choose>
              <!-- If the string contains a new line at the end. This code can't be extract as far as I know due to a bug -->
                <xsl:when test="contains($pString,'&#xa;')">
                  <xsl:variable name="pString2" select="substring-before($pString, '&#xa;')" />
                    <xsl:choose>
                    <!-- If the string contains ## or # we get just with the part after the # -->
                      <xsl:when test="starts-with($pString2, '## ')">
                        <p  class="text-lg">
                            <xsl:value-of select="substring-after($pString2,'# ')"/>
                        </p>
                      </xsl:when>
                      <xsl:when test="starts-with($pString2, '# ')">
                        <p  class="text-xl">
                            <xsl:value-of select="substring-after($pString2,'# ')"/>
                        </p>
                      </xsl:when>
                      <xsl:otherwise>
                        <p>
                          <xsl:value-of select="substring-after($pString2,'# ')"/>
                        </p>
                      </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:choose>
                  <!-- If the string contains ## or # we get just with the part after the # -->
                    <xsl:when test="starts-with($pString2, '## ')">
                      <p  class="text-xl">
                          <xsl:value-of select="substring-after($pString,'# ')"/>
                      </p>
                    </xsl:when>
                    <xsl:when test="starts-with($pString, '# ')">
                      <p  class="text-3xl">
                          <xsl:value-of select="substring-after($pString,'# ')"/>
                      </p>
                    </xsl:when>
                    <xsl:otherwise>
                      <p>
                        <xsl:value-of select="substring-after($pString,'# ')"/>
                      </p>
                    </xsl:otherwise>
                  </xsl:choose>
                </xsl:otherwise>
              </xsl:choose>
              
            </xsl:when>
            <xsl:otherwise>
                <xsl:choose>
                  <xsl:when test="contains($pString, '__')">
                      <p>
                          <xsl:call-template name="inline">
                              <xsl:with-param name="pString" select="$pString"/>
                          </xsl:call-template>
                      </p>
                  </xsl:when>
                  <xsl:when test="contains($pString, '*')">
                      <p>
                          <xsl:call-template name="inline">
                              <xsl:with-param name="pString" select="$pString"/>
                          </xsl:call-template>
                      </p>
                  </xsl:when>
                  <xsl:otherwise>
                      <p>
                          <xsl:value-of select="$pString"/>
                      </p>
                      
                  </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:call-template name="paragraph">
            <xsl:with-param name="pString"
            select="substring-after($pString,'&#xA;')"/>
        </xsl:call-template>
    </xsl:template>
    <xsl:template name="afterlist">
        <xsl:param name="pString"/>
        <xsl:choose>
            <xsl:when test="starts-with($pString,'- ')">
                <xsl:call-template name="afterlist">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,'&#xA;')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$pString"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="listItem">
        <xsl:param name="pString"/>
        <xsl:if test="starts-with($pString,'- ')">
            <!-- If the string has a new line at the end, we get the part before the new line.
                 If not, that means that is the last element so we just need to get that string without '- '  -->
            <xsl:choose>
                <xsl:when test="contains($pString,'&#xA;')">
                    <li class="ml-2 list-disc">
                        <xsl:call-template name="inline">
                            <xsl:with-param name="pString"
                            select="substring-before(substring($pString,3),'&#xA;')"/>
                        </xsl:call-template>
                    </li>
                </xsl:when>
                <xsl:otherwise>
                    <li class="ml-2 list-disc">
                        <xsl:call-template name="inline">
                            <xsl:with-param name="pString"
                            select="substring($pString,3)"/>
                        </xsl:call-template>
                    </li>
                </xsl:otherwise>
            </xsl:choose>
            <!-- Here we call the rest of the list -->
            <xsl:call-template name="listItem">
                <xsl:with-param name="pString"
                select="substring-after($pString,'&#xA;')"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <xsl:template name="inline">
        <xsl:param name="pString" select="."/>
        <xsl:if test="$pString != ''">
            <xsl:choose>
                <xsl:when test="starts-with($pString,'__')">
                    <xsl:call-template name="strong">
                        <xsl:with-param name="pString"
                        select="substring($pString,3)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="starts-with($pString,'*')">
                    <xsl:call-template name="span">
                        <xsl:with-param name="pString"
                        select="substring($pString,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="starts-with($pString,'&quot;')">
                    <xsl:call-template name="link">
                        <xsl:with-param name="pString"
                        select="substring($pString,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring($pString,1,1)"/>
                    <xsl:call-template name="inline">
                        <xsl:with-param name="pString"
                        select="substring($pString,2)"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    <xsl:template name="strong">
        <xsl:param name="pString"/>
        <xsl:variable name="vInside" select="substring-before($pString,'__')"/>
        <xsl:choose>
            <xsl:when test="$vInside != ''">
                <strong>
                    <xsl:value-of select="$vInside"/>
                </strong>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,'__')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="'__'"/>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString" select="$pString"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="span">
        <xsl:param name="pString"/>
        <xsl:variable name="vInside" select="substring-before($pString,'*')"/>
        <xsl:choose>
            <xsl:when test="$vInside != ''">
                <span class="italic">
                    <xsl:value-of select="$vInside"/>
                </span>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,'*')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="'*'"/>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString" select="$pString"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="link">
        <xsl:param name="pString"/>
        <xsl:variable name="vInside" 
               select="substring-before($pString,'&quot;')"/>
        <xsl:choose>
            <xsl:when test="$vInside != ''">
                <xsl:call-template name="href">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,'&quot;')"/>
                    <xsl:with-param name="pInside" select="$vInside"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="'&quot;'"/>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString" select="$pString"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="href">
        <xsl:param name="pString"/>
        <xsl:param name="pInside"/>
        <xsl:variable name="vHref"
        select="substring-before(substring($pString,2),']')"/>
        <xsl:choose>
            <xsl:when test="starts-with($pString,'[') and $vHref != ''">
                <a href="{$vHref}">
                    <xsl:value-of select="$pInside"/>
                </a>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString"
                    select="substring-after($pString,']')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="concat('&quot;',$pInside,'&quot;')"/>
                <xsl:call-template name="inline">
                    <xsl:with-param name="pString" select="$pString"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


</xsl:stylesheet>