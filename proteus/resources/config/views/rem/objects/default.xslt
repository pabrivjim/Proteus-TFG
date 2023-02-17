<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt"
  xmlns:proteus="https://proteus.us.es" exclude-result-prefixes="exslt msxsl">
  <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

  <xsl:template name="default" match="default" mode="call-template">
    <div class="border-4 border-blue-300 my-5" id="{@id}">
      <h5 class="bg-blue-200 p-1">
        <span class="secno">4.3.2.1 </span>
        <xsl:value-of select="properties/*[@name='name']" disable-output-escaping="yes"/>
      </h5>
      <div class="summary">
        <p class="p-2 border-b-2 border-blue-200">
            Description
        </p>
        <table class="m-3">
          <tbody class="text-left">
            <xsl:for-each select="properties/*">
              <xsl:if test=". != 'PD'">
                <tr>
                  <th class="capitalize align-top">
                    <xsl:value-of select="@name" disable-output-escaping="yes"/>
                  </th>
                  <td class="pl-5">
                    <ul>
                      <li>
                        <xsl:value-of select="." disable-output-escaping="yes"/>
                      </li>
                    </ul>
                  </td>
                </tr>
              </xsl:if>
            </xsl:for-each>
          </tbody>
        </table>
      </div>
    </div>
  </xsl:template>

</xsl:stylesheet>